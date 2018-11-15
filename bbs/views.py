from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bbs.models import Post


def my_login(request):
    return render(request, 'bbs/login.html')


def login_func(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'bbs/login.html')


def logout_func(request):
    logout(request)
    return render(request, 'bbs/login.html')


@login_required(login_url='login')
def index(request):
    posts = Post.objects.all().order_by('-is_top', '-last_time')
    return render(request, 'bbs/index.html', {'posts': posts})


@login_required(login_url='login')
def test(request):
    return render(request, 'bbs/base2.html')
