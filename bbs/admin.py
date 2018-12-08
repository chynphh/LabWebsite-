from django.contrib import admin
from .models import Post, MyUser, Reply, Comment
from django.db import models

# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('content_html',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(MyUser, MyUserAdmin)


from martor.widgets import AdminMartorWidget
from .models import Martor

class MartorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(Martor, MartorAdmin)