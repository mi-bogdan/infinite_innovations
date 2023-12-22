from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.views.generic.base import View
from django.views.generic import TemplateView

from .forms import LoginForms, RegisterForm



class LoginUser(View):
    def post(self, request):
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')

    def get(self, request):
        context = {'login_forms': LoginForms()}
        return render(request, 'authentications/login.html', context)


class RegisterUser(TemplateView):
    """Регистрация"""
    template_name = 'authentications/register.html'

    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')


def logout_user(request):
    """Выход с системы"""
    logout(request)
    return redirect('index')
