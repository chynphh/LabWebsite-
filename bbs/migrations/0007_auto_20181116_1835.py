# Generated by Django 2.1.3 on 2018-11-16 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0006_auto_20181116_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content_html',
            field=models.TextField(),
        ),
    ]
