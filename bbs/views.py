from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def my_login(request):
    return render(request, 'bbs/login.html')


def login_func(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'bbs/index.html')
    else:
        return render(request, 'bbs/login.html')


@login_required(login_url='login')
def index(request):
    return render(request, 'web/home.html')


def logout_func (request):
    logout(request)
    return render(request, 'bbs/login.html')
