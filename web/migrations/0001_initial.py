# Generated by Django 2.1.1 on 2018-11-14 17:09

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', ckeditor.fields.RichTextField(verbose_name='实验室简介')),
            ],
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='img/carousel', verbose_name='图片')),
                ('title', models.TextField(blank=True, verbose_name='简介')),
                ('link', models.URLField(blank=True, verbose_name='文章链接')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='标题')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日期')),
                ('news_type', models.CharField(choices=[('Paper', 'Paper'), ('Application', 'Application'), ('News', 'News')], default=('News', 'News'), max_length=20, verbose_name='新闻类别')),
                ('detial', ckeditor.fields.RichTextField(verbose_name='正文')),
                ('view', models.IntegerField(default=1, verbose_name='浏览量')),
            ],
        ),
        migrations.CreateModel(
            name='Publictaion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('link', models.URLField(blank=True, verbose_name='文章链接')),
                ('code', models.URLField(blank=True, verbose_name='代码链接')),
                ('year', models.IntegerField(verbose_name='发表年份')),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日期')),
                ('intro', models.TextField(verbose_name='简介')),
                ('tag1', models.CharField(blank=True, max_length=20, verbose_name='标签一')),
                ('tag2', models.CharField(blank=True, max_length=20, verbose_name='标签二')),
                ('tag3', models.CharField(blank=True, max_length=20, verbose_name='标签三')),
                ('link', models.URLField(blank=True, verbose_name='链接')),
                ('image', models.ImageField(help_text='必须上传尺寸为500x600的图片，否则显示会有问题。', upload_to='img/research', verbose_name='图片')),
                ('detial', ckeditor.fields.RichTextField(verbose_name='正文')),
                ('view', models.IntegerField(default=1, verbose_name='浏览量')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('student_type', models.CharField(choices=[('Ph.D.', '博士生'), ('M.S.', '硕士生'), ('Undergraduates', '本科生')], default=('Undergraduates', '本科生'), max_length=20, verbose_name='学生类别')),
                ('status', models.BooleanField(default=True, verbose_name='是否在读')),
                ('homepage', models.URLField(blank=True, verbose_name='个人主页')),
                ('github', models.URLField(blank=True, verbose_name='Github')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='邮箱')),
                ('research_interests', models.TextField(blank=True, default='强化学习；深度学习；', verbose_name='研究方向')),
                ('image', models.ImageField(help_text='必须上传尺寸为400x550的图片，否则显示会有问题。', upload_to='img/member', verbose_name='个人照片')),
                ('year', models.IntegerField(default=2018, verbose_name='入学年份')),
            ],
        ),
    ]
