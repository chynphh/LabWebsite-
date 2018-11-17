# Generated by Django 2.1.3 on 2018-11-18 01:46

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0012_auto_20181117_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(default='avatar/default.png', upload_to='avatar', verbose_name='头像'),
        ),
    ]
