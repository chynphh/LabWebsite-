from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from ckeditor.fields import RichTextField
import django.utils.timezone as timezone
from DjangoUeditor.models import UEditorField
from django.urls import reverse


class MyUserManager(BaseUserManager):
    def create_user(self, username, name, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(user_name, name,
                                password=password
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(u'账号', max_length=50)
    password = models.CharField(u'密码', max_length=50)
    name = models.CharField(u'姓名', max_length=50)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()  # 实例化类,这个必须要有

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'name']  # 必须填写的字段

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        # self.password = make_password(raw_password)
        self.password = raw_password

    def check_password(self, password):
        # return check_password(raw_password, self.password)
        return password == self.password

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Post(models.Model):
    status_choice = (
        (u'Closed.', u'已关闭'),
        (u'Open.', u'开放中'),
    )
    title = models.CharField(u'标题', max_length=50)
    # 创建时间上和更新时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_time = models.DateTimeField(auto_now=True, verbose_name='最后回复时间')

    status = models.CharField(
        u'帖子状态', max_length=20, choices=status_choice, default=status_choice[1])
    view = models.IntegerField(u'浏览量', default=1)
    reply = models.IntegerField(u'回复量', default=0)
    # content_html = UEditorField(imagePath="/img/",
    #                             filePath="media/img/", verbose_name=u"文章内容")
    content_html = models.TextField(verbose_name=u"文章内容")
    is_top = models.BooleanField(u'是否置顶', default=True)

    # 定义外键关系
    author = models.ForeignKey(
        MyUser, verbose_name='作者', on_delete=models.CASCADE)
    # creator_id = models.IntegerField(u'创建者ID')

    def increase_view(self):
        self.view += 1
        self.save(update_fields=['view'])

    def increase_reply(self):
        self.reply += 1
        self.save(update_fields=['reply'])

    def __str__(self):  # __str__ on Python 3
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    class Meta:
        app_label = 'bbs'


class Reply(models.Model):
    post = models.ForeignKey(
        Post, related_name='reply_set', on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    # content_html = UEditorField(imagePath="/img/",
    #                             filePath="media/img/", verbose_name=u"回复内容")
    content_html = models.TextField(verbose_name=u"回复内容")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):  # __str__ on Python 3
        return f"reply to"

    class Meta:
        app_label = 'bbs'


class Comment(models.Model):
    reply = models.ForeignKey(
        Reply, related_name='comment_set', on_delete=models.CASCADE)
    user = models.ForeignKey(
        MyUser, related_name='comment_user_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        MyUser, related_name='comment_user_to_set', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # content = UEditorField(imagePath="/img/",
    #                             filePath="media/img/", verbose_name=u"评论内容")
    content = models.TextField(verbose_name=u'评论内容')

    def __str__(self):  # __str__ on Python 3
        return f"comment...."

    class Meta:
        app_label = 'bbs'
