from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bbs.models import Post, Reply, Comment, MyUser
from bbs.forms import PostForm, ReplyForm, CommentForm, UserForm


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
def upload(request):
    print(request.POST)
    print(request.FILES)

    return render(request, 'bbs/test.html')


@login_required(login_url='login')
def profile(request):
    profile_messages = []
    posts = request.user.post_set.all()
    if request.method == 'POST':
        passwd_check = True
        print(request.POST)
        currentPassword = request.POST['currentPassword']
        newPassword = request.POST['newPassword']
        confirmNewPassword = request.POST['confirmNewPassword']
        uploadImg = request.FILES.get('uploadImg')
        if currentPassword != '':
            if not request.user.check_password(currentPassword):
                profile_messages.append('密码不正确')
                passwd_check = False
            elif newPassword == '' or confirmNewPassword == '':
                profile_messages.append('密码不能为空')
                passwd_check = False
            elif newPassword != confirmNewPassword:
                profile_messages.append('两次密码不一致')
                passwd_check = False
        if passwd_check:
            new_name = request.POST['name']
            if new_name != '':
                request.user.name = new_name
                if newPassword != '':
                    request.user.set_password(newPassword)
                if uploadImg is not None:
                    request.user.avatar = uploadImg
                request.user.save()
                profile_messages.append('资料修改成功！')
            else:
                profile_messages.append('名称不能为空')
    return render(request, 'bbs/profile.html', context={'posts':posts, 'profile_messages': profile_messages})


@login_required(login_url='login')
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reply_form = ReplyForm()
    comment_form = CommentForm()
    post.increase_view()
    reply_list = post.reply_set.all().order_by('created_time')
    comment_list = []
    for reply in reply_list:
        cur_list = reply.comment_set.all().order_by('created_time')
        comment_list.append(cur_list)
    return render(request, 'bbs/detail.html', locals())


@login_required
def add_comment(request, reply_pk, user_to_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)
    post = reply.post
    user_to = get_object_or_404(MyUser, pk=user_to_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.reply = reply
            comment.user_to = user_to
            comment.save()
            # print(comment)
            post.save()

            print('add reply success')
            return redirect(post)
        else:
            reply_form = ReplyForm()
            reply_list = post.reply_set.all().order_by('created_time')
            comment_list = []
            for reply in reply_list:
                cur_list = reply.comment_set.all().order_by('created_time')
                comment_list.append(cur_list)
            context = {'post': post,
                       'reply_form': reply_form,
                       'comment_form': comment_form,
                       'reply_list': reply_list,
                       'comment_list': comment_list,
                       }
            return render(request, 'bbs/detail.html', context=context)
    return redirect(post)


@login_required
def add_reply(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.save()
            post.increase_reply()
            post.save()
            print('add reply success')
            return redirect(post)
        else:
            comment_form = CommentForm()
            reply_list = post.reply_set.all().order_by('created_time')
            comment_list = []
            for reply in reply_list:
                cur_list = reply.comment_set.all().order_by('created_time')
                comment_list.append(cur_list)
            context = {'post': post,
                       'comment_form': comment_form,
                       'reply_form': reply_form,
                       'reply_list': reply_list,
                       'comment_list': comment_list,
                       }
            return render(request, 'bbs/detail.html', context=context)
    return redirect(post)


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

@login_required(login_url='login')
def delete(request, delete_type, pk):
    print(delete_type, pk)
    print(request.path)
    print(request.get_full_path())
    if delete_type == 'post':
        obj = get_object_or_404(Post, pk=pk)
        if request.user == obj.author:
            obj.delete()
        return redirect(request.user)
    elif delete_type == 'reply':
        obj = get_object_or_404(Reply, pk=pk)
        post = obj.post
        post.decrease_reply()
        if request.user == obj.user:
            obj.delete()
        return redirect(post)
    elif delete_type == 'comment':    
        obj = get_object_or_404(Comment, pk=pk)
        post = obj.reply.post

        if request.user == obj.user:
            obj.delete()
        return redirect(post)
        
