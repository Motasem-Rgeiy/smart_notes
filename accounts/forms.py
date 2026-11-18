from django import forms
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm , UserChangeForm
from notes_app.models import User


class UserLoginForm(AuthenticationForm):
    def  __init__(self, request = ..., *args, **kwargs):
        super(UserLoginForm , self).__init__(*args, **kwargs)


    username = forms.CharField(
        label='',
        widget=forms.TextInput({'class':'bg-slate-950 w-full p-2 rounded-lg'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput({'class':'bg-slate-950 w-full p-2 rounded-lg'})
    )

  
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget= forms.TextInput({'class':'bg-slate-950 w-full p-2 rounded-lg'})
    )
    last_name = forms.CharField(
        widget= forms.TextInput({'class':'bg-slate-950 w-full p-2 rounded-lg'})
    )
    username = forms.CharField(
        widget= forms.TextInput({'class':'bg-slate-950 w-full p-2 rounded-lg'})
    )
    email = forms.CharField(
        widget= forms.TextInput({'class':'bg-slate-950 w-full p-2 rounded-lg'})
    )
    password1 = forms.CharField(
        widget= forms.PasswordInput({'class':'bg-slate-950 w-full p-2 rounded-lg'})
    )
    password2 = forms.CharField(
        widget= forms.PasswordInput({'class':'bg-slate-950 w-full p-2 rounded-lg'})
    )

    class Meta:
        model = User #Error: Reason: i've customized the user, so i have to use the customized model of it
        fields = ["first_name" , 'last_name' , 'username' , 'email' , ]#'image']


class ProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email' , 'image']
        widgets = {
            'first_name':forms.TextInput({'class':'bg-slate-950 w-full p-2 rounded-lg'}),
            'last_name':forms.TextInput({'class':'bg-slate-950 w-full p-2 rounded-lg'}),
            'email':forms.TextInput({'class':'bg-slate-950 w-full p-2 rounded-lg'}),
            'image': forms.FileInput({'class':'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-slate-800 file:text-slate-100 hover:file:bg-slate-700 cursor-pointer'})

        }