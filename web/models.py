# coding:utf-8
from django.db import models
import datetime
import django.utils.timezone as timezone
from ckeditor.fields import RichTextField

# Create your models here.


class Carousel(models.Model):
    image = models.ImageField(u'图片', upload_to='img/carousel', height_field=None,
                              width_field=None)
    title = models.TextField(u'简介', blank=True)
    link = models.URLField(u'文章链接', blank=True) 
    class Meta:
        app_label = 'web'

class Student(models.Model):
    student_type_choice = (
        (u'Postdoc.', u'博士后'),
        (u'Ph.D.', u'博士生'),
        (u'M.S.', u'硕士生'),
        (u'Undergraduates', u'本科生'),
    )
    today = datetime.date.today()

    name = models.CharField(u'姓名', max_length=50)
    student_type = models.CharField(
        u'学生类别', max_length=20, choices=student_type_choice, default=student_type_choice[2])
    status = models.BooleanField(u'是否在读', default=True)
    homepage = models.URLField(u'个人主页', blank=True)
    github = models.URLField(u'Github', blank=True)
    email = models.EmailField(u'邮箱', blank=True)
    research_interests = models.TextField(
        u'研究方向', default=u'强化学习；深度学习；', blank=True)
    image = models.ImageField(u'个人照片', upload_to='img/member', height_field=None,
                              width_field=None, max_length=100, help_text='必须上传尺寸为400x550的图片，否则显示会有问题。')
    year = models.IntegerField(u'入学年份', default=today.year)

    class Meta:
        app_label = 'web'
    def __str__(self):  # __str__ on Python 3
        return self.name


class Publictaion(models.Model):
    title = models.CharField(u'标题', max_length=200)
    link = models.URLField(u'文章链接', blank=True)
    code = models.URLField(u'代码链接', blank=True)
    year = models.IntegerField(u'发表年份')

    class Meta:
        app_label = 'web'
    def __str__(self):
        return self.title


class About(models.Model):
    about = RichTextField(u'实验室简介')
    class Meta:
        app_label = 'web'


class Research(models.Model):
    title = models.CharField(u'标题', max_length=100)
    date = models.DateTimeField('日期', default=timezone.now)
    intro = models.TextField(u'简介')
    tag1 = models.CharField(u'标签一', max_length=20, blank=True)
    tag2 = models.CharField(u'标签二', max_length=20, blank=True)
    tag3 = models.CharField(u'标签三', max_length=20, blank=True)
    link = models.URLField(u'链接', blank=True)
    image = models.ImageField(u'图片', upload_to='img/research', height_field=None,
                              width_field=None, max_length=100, help_text='必须上传尺寸为500x600的图片，否则显示会有问题。')

    detail = RichTextField('正文')
    view = models.IntegerField(u'浏览量', default=1)

    def increase_views(self):
        self.view += 1
        self.save(update_fields=['view'])

    class Meta:
        app_label = 'web'
    def __str__(self):
        return self.title


class News(models.Model):
    title = models.TextField(u'标题')
    date = models.DateTimeField('日期', default=timezone.now)

    news_type_choice = (
        (u'Paper', u'Paper'),
        (u'Application', u'Application'),
        (u'News', u'News'),
    )
    news_type = models.CharField(
        u'新闻类别', max_length=20, choices=news_type_choice, default=news_type_choice[2])

    detail = RichTextField('正文')
    view = models.IntegerField(u'浏览量', default=1)

    def increase_views(self):
        self.view += 1
        self.save(update_fields=['view'])

    class Meta:
        app_label = 'web'
    def __str__(self):
        return self.title
