from lib2to3.fixes.fix_input import context

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View

from accounts.forms import LoginForm, RegisterForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user=authenticate(username=data['username'],password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('You are now logged in')
                else:
                    return HttpResponse('Your registration is disabled')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()
        context = {'form':form}
    return render(request, 'registration/login.html', context)


def dashboard_view(request):
    user=request.user
    context={'user':user}
    return render(request,'pages/dashboard.html')

def user_register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user':new_user})

    else:
        user_form = RegisterForm()

    context = {'user_form':user_form}
    return render(request, 'registration/register.html', context)

class SignupView(CreateView):
    form_class = UserCreationForm
    print(form_class)
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
