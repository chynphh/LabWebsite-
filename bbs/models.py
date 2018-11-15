from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from ckeditor.fields import RichTextField
import django.utils.timezone as timezone


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
    last_time = models.DateTimeField('最后回复时间', default=timezone.now)
    status = models.CharField(
        u'帖子状态', max_length=20, choices=status_choice, default=status_choice[1])
    creator_id = models.IntegerField(u'创建者ID')
    view = models.IntegerField(u'浏览量', default=1)
    reply = models.IntegerField(u'回复量', default=0)
    content = models.TextField(u'内容')
    is_top = models.BooleanField(u'是否置顶', default=True)

    def increase_view(self):
        self.view += 1
        self.save(update_fields=['view'])

    def increase_reply(self):
        self.reply += 1
        self.save(update_fields=['reply'])

    def __str__(self):  # __str__ on Python 3
        return self.title

    class Meta:
        app_label = 'bbs'


# class Reply(models.Model):
#     post_id = models.IntegerField()
#     creator_id = models.IntegerField(u'创建者ID')
#     content = models.TextField(u'内容')
#     time = models.DateTimeField('时间', default=timezone.now)
#     comment = models.IntegerField(u'评论量', default=0)

#     def __str__(self):  # __str__ on Python 3
#         return f"{self.creator_id},{self.time}"

#     class Meta:
#         app_label = 'bbs'


# class Comment(models.Model):
#     reply_id = models.IntegerField()
#     creator_id = models.IntegerField(u'创建者ID')
#     content = models.TextField(u'内容')
#     time = models.DateTimeField('时间', default=timezone.now)

#     def __str__(self):  # __str__ on Python 3
#         return f"{self.creator_id},{self.time}"

#     class Meta:
#         app_label = 'bbs'
