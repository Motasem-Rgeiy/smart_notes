from django import forms
from notes_app import models


atters = {'class':'bg-red-700'}
class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ['title' , 'description' , 'image' , 'uploaded_file' , 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class':'bg-slate-950 w-full p-2 focus:outline-1'}),
            'description': forms.Textarea(attrs={'class':'bg-slate-950 w-full h-32 p-2 focus:outline-1'}),
            'image':forms.FileInput({'class':'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-slate-800 file:text-slate-100 hover:file:bg-slate-700 cursor-pointer'}),
            'uploaded_file': forms.FileInput({'class':'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-slate-800 file:text-slate-100 hover:file:bg-slate-700 cursor-pointer'}),
            'category': forms.Select({'class':"w-fit"}),
        }


    def __init__(self, *args, **kwargs):
        # Extract the user passed from the view
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter categories to only show those owned by the current user
        if user:
            self.fields['category'].queryset = models.Category.objects.filter(user=user)




class NoteUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ['title' , 'description' , 'status' , 'category' ,'uploaded_file', 'image']
        labels = {
            'image':'Image'
        }
        widgets = {
            'title':forms.TextInput({'class':"bg-slate-950 p-1 rounded-lg text-base focus:outline-1"}),
            'description':forms.Textarea({'class':'bg-slate-950 p-3 w-full focus:outline-1'}),
            'image': forms.FileInput(),
            'uploaded_file': forms.FileInput({'class':'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-slate-800 file:text-slate-100 hover:file:bg-slate-700 cursor-pointer'}),
            'image': forms.FileInput({'class':'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-slate-800 file:text-slate-100 hover:file:bg-slate-700 cursor-pointer'})

          
        }

    def __init__(self, *args, **kwargs):
            # Extract the user passed from the view
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
    
            # Filter categories to only show those owned by the current user
            if user:
                self.fields['category'].queryset = models.Category.objects.filter(user=user)




class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput({'class':"bg-slate-950 p-2 rounded-lg text-base focus:outline-1 "})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)



    def clean_name(self):
        name = self.cleaned_data.get('name')
        if models.Category.objects.filter(name__iexact=name, user = self.user).exists():
            raise forms.ValidationError(f'The category "{name}" already exists.')
        return name

 