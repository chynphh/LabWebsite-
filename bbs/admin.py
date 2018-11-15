from django.contrib import admin
from .models import MyUser, Post

# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Post, PostAdmin)
admin.site.register(MyUser, MyUserAdmin)
