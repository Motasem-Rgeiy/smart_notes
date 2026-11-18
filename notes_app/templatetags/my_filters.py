from django import template

register = template.Library()

def title_cut(title):
    print('Here is tamplet tags')
    if not title:
        return 'Untitled'
    if len(title) <= 20:
        return title
    
    return title[:20] + '. '*15

def profile_name_cut(name):
    if not name:
        return 'Unnamed'
    if len(name) <= 5:
        return name

    return name[:5] + '..'


register.filter('cut' , title_cut)
register.filter('cut_name', profile_name_cut)
