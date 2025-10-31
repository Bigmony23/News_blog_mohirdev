from lib2to3.fixes.fix_input import context

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from .models import Profile
from accounts.forms import LoginForm, RegisterForm, UserEditForm, ProfileEditForm
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

@login_required
def dashboard_view(request):
    user=request.user
    profile=request.user.profile
    context={'user':user,'profile':profile}
    return render(request,'pages/dashboard.html',context)


def user_register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()
            Profile.objects.create(user=new_user)
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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render(request,'registration/profile_edit.html',{'user_form':user_form,'profile_form':profile_form})

class EditUserView(LoginRequiredMixin,View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'registration/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
    def post(self, request):
        if request.method == 'POST':
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('user_profile')
