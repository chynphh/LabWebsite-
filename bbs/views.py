from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bbs.models import Post, Reply, Comment, MyUser
from bbs.forms import PostForm, ReplyForm, CommentForm, UserForm, MartorForm
from notifications.models import Notification
from bbs.email import send_text_email

import os
import json
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from martor.utils import LazyEncoder

# 修改未读消息为已读装饰器
def notifications_read(func):
    def wrapper(request, *args, **kwargs):
        # print(request.get_full_path())
        notify_key = 'notification'
        if request.GET.get(notify_key):
            try:
                # 获取消息
                notify_id = int(request.GET[notify_key])
                notify = Notification.objects.get(pk=notify_id)
                # 标记为已读
                notify.unread = False
                notify.save()
            except ValueError:
                # int转换错误，不处理
                pass
            except Notification.DoesNotExist:
                # 消息不存在，不处理
                pass
        return func(request, *args, **kwargs)
    return wrapper


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

        email_check = True
        email = request.POST['email']
        mailnotify = bool(request.POST.get('mailnotify', False))
        if mailnotify:
            if email == '':
                profile_messages.append('邮箱不能为空')
                email_check = False
        try:
            request.user.email = email
            request.user.mailnotify = mailnotify
        except Exception as e:
            profile_messages.append('邮箱格式不对')
            email_check = False

        if passwd_check and email_check:
            new_name = request.POST['name']
            if new_name != '':
                request.user.name = new_name
                request.user.email
                if newPassword != '':
                    request.user.set_password(newPassword)
                if uploadImg is not None:
                    request.user.avatar = uploadImg
                request.user.save()
                profile_messages.append('资料修改成功！')
            else:
                profile_messages.append('名称不能为空')
    return render(request, 'bbs/profile.html', context={'posts':posts, 'profile_messages': profile_messages})


@notifications_read
@login_required(login_url='login')
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reply_form = ReplyForm()
    comment_form = CommentForm()
    post.increase_view()
    reply_list = post.reply_set.all().order_by('created_time')
    comment_list = []
    comment_form_list = []
    for reply in reply_list:
        cur_list = reply.comment_set.all().order_by('created_time')
        comment_list.append(cur_list)
        comment_form_list.append(CommentForm())
    return render(request, 'bbs/detail.html', locals())


@login_required(login_url='login')
def add_comment(request, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)
    post = reply.post
    if request.method == 'POST':
        user_to_pk = request.POST['user_to']
        user_to = get_object_or_404(MyUser, pk=user_to_pk)

        comment = Comment()
        comment.content=request.POST[f'content{reply_pk}']
        comment.user = request.user
        comment.reply = reply
        comment.user_to = user_to
        comment.save()
        post.save()
        return redirect(post)

        # comment_form = CommentForm(request.POST)
        # if comment_form.is_valid():
        #     comment = comment_form.save(commit=False)
        #     comment.user = request.user
        #     comment.reply = reply
        #     comment.user_to = user_to
        #     comment.save()
        #     # print(comment)
        #     post.save()
        #     return redirect(post)
        # else:
        #     reply_form = ReplyForm()
        #     reply_list = post.reply_set.all().order_by('created_time')
        #     comment_list = []
        #     for reply in reply_list:
        #         cur_list = reply.comment_set.all().order_by('created_time')
        #         comment_list.append(cur_list)
        #     context = {'post': post,
        #                'reply_form': reply_form,
        #                'comment_form': comment_form,
        #                'reply_list': reply_list,
        #                'comment_list': comment_list,
        #                }
        #     return render(request, 'bbs/detail.html', context=context)
    return redirect(post)


@login_required(login_url='login')
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

@login_required(login_url='login''bbs/detail.html',)
def user_mark_all_read(request):
    user = request.user
    notifies = user.notifications.unread()
    notifies.mark_all_as_read()  # 标记所有未读为已读
    return redirect('index')

def test(request):
    form = MartorForm()
    return render(request, 'bbs/test.html', {'form': form})

def test_post(request):
    new_form = MartorForm()
    if request.method == 'POST':
        form = MartorForm(request.POST)
        form.save()
        return redirect('index')
    return render(request, 'bbs/test.html', {'form': new_form})


@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    print('fark2131231')
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            # print(dir(image))
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))
