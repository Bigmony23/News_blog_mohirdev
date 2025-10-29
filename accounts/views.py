from lib2to3.fixes.fix_input import context

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from accounts.forms import LoginForm


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
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


