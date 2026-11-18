from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from accounts import forms
from django.urls import reverse , reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.



class UserRegisterView(generic.CreateView):
    form_class = forms.UserRegisterForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        login(self.request , self.object)
        return reverse_lazy('note_list')

class UserChangeView(LoginRequiredMixin, generic.UpdateView):
    
    form_class = forms.ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset = None):
        print(self.request.user)
        return self.request.user