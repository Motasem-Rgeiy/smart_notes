from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse ,Http404 , FileResponse , JsonResponse , HttpResponseBadRequest , StreamingHttpResponse
from django.views import generic
from notes_app import models , forms
from django.urls import reverse
from django.db.models import Q
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
import json
from notes_app.export_files import pdf_generation , txt_generation , json_generation , csv_generation
import smtplib
from django.conf import settings
from notes_app.webScraping import getNews , get_data
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from notes_app.ai_api_process import content_process_gemini, chatbot_assistant
# Create your views here.






#List Notes by user requirements
class NoteListView(LoginRequiredMixin, generic.ListView):
    model =  models.Note
    template_name = 'notes/notes_list.html'
    paginate_by = 6

    def get_queryset(self):
        if not self.request.session:
            self.request.session.create()
        
        allowed_sort_fields = ['updated_at' , 'created_at']
        target_notes = super().get_queryset().filter(user = self.request.user)
        q = self.request.GET.get('q' , None)
        order_by = self.request.GET.get('order' , None)


        category_id = self.request.GET.get('ca' ,None)
        print('My category id = ' , category_id)
        
        #None will be as a string, not boolean
        if  category_id and category_id not in ['None', 'null', '']:
            print('input cat id, ' ,category_id )
            self.request.session['category_id'] = category_id
            print('view cat id, ',self.request.session['category_id'])
            target_notes = target_notes.filter(category_id = category_id)
        else:
            self.request.session['category_id'] = 0
    
        if not order_by and order_by not in allowed_sort_fields:
            order_by = self.request.session.get('order1' , 'created_at')

        self.request.session['order1'] = order_by

        if self.request.session['order1'] == 'created_at':
            self.request.session['order2'] = 'updated_at'
        else:
            self.request.session['order2'] = 'created_at'

        print(self.request.session['order1'])
        print(self.request.session['order2'])

        

        if q:
           return target_notes.filter(Q(title__icontains=q) | Q(description__icontains=q)).order_by(f"-{order_by}")
        return target_notes.order_by(f'-{order_by}')



        

        
#Create Note
class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Note
    form_class = forms.NoteCreateForm
    template_name = 'notes/note_create.html'

    def get_success_url(self):
        return reverse('note_list')

    def form_valid(self, form):
            form.instance.user = self.request.user
            if form.is_valid():
                form.save()
                if self.request.user.email:
                    email = self.request.user.email
                    title = f"title: '{form.cleaned_data['title']}'"

                    if not title:
                        title = 'Untitled'

                    body = """Subject: New Note has been created successfuly.\nDear %s\nYou have created a new Note with %s
You can read this note at any given time you want by openning the application.""" %(self.request.user.first_name, title)

                    
                    smptObj = smtplib.SMTP('smtp.gmail.com' ,587)
                    smptObj.starttls()
                    smptObj.login(settings.SENDER_EMAIL , settings.EMAIL_PASSWORD)
                    

                    smptObj.sendmail(settings.SENDER_EMAIL , email , body)
    
            return super().form_valid(form)



    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs







#Update Note
class NoteUpdateView(LoginRequiredMixin , UserPassesTestMixin, generic.UpdateView):
    model = models.Note
    form_class = forms.NoteUpdateForm
    template_name = 'notes/note_update.html'
    

    def get_success_url(self):
        return reverse('note_update' ,args=[self.object.id])

    #Track the errors on the terminal
    def form_invalid(self, form):
        print("Form validation failed:", form.errors)
        return super().form_invalid(form)

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['user'] = self.request.user
            return kwargs


    def test_func(self):
        return self.get_object().user_id == self.request.user.id
    


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = models.Note
    template_name = 'notes/note_delete.html'

    def get_success_url(self):
        return reverse('note_list')

    def test_func(self):
        return self.get_object().user_id == self.request.user.id







#Download the image of a note immediately to the user's browser
@login_required
def download_image(request , pk):
    note = get_object_or_404(models.Note , pk = pk)
  
    try:
        response = FileResponse(
            note.image.open('rb'),
            as_attachment=True,
            filename=note.image.name.split('/')[-1] #Get the last name of a complete absolute path if i use upload_to parameter in the models.py.
        )
        return response
    except FileNotFoundError:
        raise Http404('File does not exist in the server')
    except ValueError:
        raise Http404("You don't provide a file!")




    

#Create Category
class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Category
    form_class = forms.CategoryCreateForm
    template_name = 'category/category_create.html'

    def get_success_url(self):
        return reverse('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    





#Delete Category
class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin , generic.DeleteView):
    model = models.Category
    template_name = 'notes/note_delete.html'
  

    def get_success_url(self):
        return reverse('dashboard')

    def test_func(self):
        return self.get_object().user.id == self.request.user.id


#Reutrns:
    # 1- Recent 5 notes
    # 2- 4 Most used cateogries
    # 3- Category total ccount
    # 4-  Note total count
@login_required
def dashboard(request):
    print(request.session.get('order'))
    notes_count = models.Note.objects.filter(user = request.user).count()
    category_count = models.Category.objects.filter(user = request.user).count()
    categories = models.Category.objects.filter(user = request.user).annotate(total_notes = Count('notes')).order_by('-total_notes')[:4]
    most_used_cats = []
    for category in categories:
        most_used_cats.append({category.name:len(category.notes.all())})

    recent_notes = models.Note.objects.select_related('category').filter(user = request.user).order_by('-updated_at')[:4]
    
    return render(request , 'notes/dashboard.html' , {'recent_notes':recent_notes ,'note_count': notes_count , 'cat_count': category_count ,'data':most_used_cats })


    
@csrf_exempt
@login_required
def export_system(request):
    if request.method == 'POST':
        format = json.loads(request.body).get('format')
        note_id = json.loads(request.body).get('noteId')


        if not note_id:
            note_obj = models.Note.objects.select_related('category').filter(user = request.user)
        elif format != 'txt':
            note_obj = models.Note.objects.filter(pk = note_id , user = request.user)
        else:
            note_obj = models.Note.objects.filter(pk = note_id , user = request.user).last()


        if not note_obj:
             return HttpResponseBadRequest('Note is not found!')
        
        if format == 'pdf':
            response = FileResponse(pdf_generation(note_obj) , as_attachment=True)

        elif format == 'txt':
            response = FileResponse(txt_generation(note_obj) , as_attachment=True)

        elif format == 'json':
            response = FileResponse(json_generation(note_obj) , as_attachment=True)

        elif format == 'csv':
            response = FileResponse(csv_generation(note_obj) , as_attachment=True)


        return response


@csrf_exempt
@login_required
def getLatestNewsInternet(request):
    if request.method == "POST":
        titles_links = getNews()
        return JsonResponse({'data':titles_links})

@csrf_exempt
@login_required
def save_news(request):
    print(request.body)
    if request.method == "POST":
        link = json.loads(request.body).get('link')
        title = json.loads(request.body).get('title')
   
        content = get_data(link)
       # INSERT INTO cat(name) VALUES('technology') ON CONFLICT DO NOTHING;
        target_category = models.Category.objects.get_or_create(name='technology' , user = request.user)[0]

     
        models.Note.objects.create(title = title , description = content , category = target_category , user = request.user)
        return JsonResponse({'status':'success'})


@login_required
@csrf_exempt
def ai_tasks(request):
    content = json.loads(request.body).get('content')
    system_settings = json.loads(request.body).get('system_settings')
  
    ai_response = content_process_gemini(content, system_settings)

    #return JsonResponse({'summarized_content':summarized_content})
    return StreamingHttpResponse(ai_response, content_type='text/plain')


@login_required
def note_image_remove(request , pk):
    if not pk:
        return HttpResponse('Not Found')

    target_note = models.Note.objects.filter(pk = pk, user=request.user).last()
    target_note.image = None
    target_note.save()
    return redirect('note_update' , pk)



@login_required
@csrf_exempt
def ai_chatbot(request):
    if request.method == 'POST':
        user_input = json.loads(request.body).get('user_input')
        print(user_input , 'user_input')
        if not user_input:
            return JsonResponse({})

        if request.user.first_name:
            username = request.user.first_name
        else:
            username = request.user.username
        
        chatbot_response = chatbot_assistant(user_input,  username)

        #return JsonResponse({'message':chatbot_response})
        return StreamingHttpResponse(chatbot_response, content_type='text/plain')
    

    return render(request , 'ai/chatbot.html')
