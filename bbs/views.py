from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bbs.models import Post
from bbs.forms import PostForm, ReplyForm


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


@login_required(login_url='login')
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reply_form = ReplyForm()
    post.increase_views()
    if request.method == 'POST':
        # 获取前台传过来的数据，用来生成form对象
        reply_form = ReplyForm(request.POST)
        # 判断form表单数据是否合法
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.save()
            post.increase_reply()
            return redirect(post)
    return render(request, 'bbs/detail.html', {'post': post})


@login_required(login_url='login')
def add_post(request):
    form = PostForm()
    # print(form)
    # 判断request的请求方法，如果是post方法，那么就处理数据
    if request.method == 'POST':
        # 获取前台传过来的数据，用来生成form对象
        form = PostForm(request.POST)
        # 判断form表单数据是否合法
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('index')
    return render(request, 'bbs/add_post.html', locals())
