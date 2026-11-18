from notes_app import models
from django.db.models import Case, When, Value, IntegerField

def smart_notes_website(request):
    if request.resolver_match and request.resolver_match.url_name == 'login' or request.resolver_match.url_name == 'register':
        return {}
   # categories = models.Category.objects.filter(user = request.user)

    selected_category_id = request.session.get('category_id' , 0)
   


    categories = models.Category.objects.annotate(
    selected_category=Case(
        When(pk=selected_category_id, then=Value(0)),  # Top priority
        default=Value(1),                     # Normal priority
        output_field=IntegerField()
    )

).order_by('selected_category', 'name').filter(user = request.user)

    
    
    if not categories:
        return {}

    if selected_category_id == 0:
        print('all cats')
        return{
        'first_cat_id':None,
        'first_cat_name': 'All Categories',
        'categories':categories,
       
        }
    else:
        if len(categories) == 1:
                 print('Only one cat')
                 return {
                 'first_cat_name':categories[0].name,
                 'first_cat_id': categories[0].pk,
                 'categories': None,
                 'last_cat_id':None,
                 'last_cat_name':'All Categories',
                 }
        else:
            print('more than two')
            return{
            'first_cat_name' : categories[0].name,
            'first_cat_id': categories[0].pk,
            'categories':categories[1:],
            'last_cat_id': None,
            'last_cat_name':'All Categories'
            }


