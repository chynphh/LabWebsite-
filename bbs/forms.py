from django import forms
from .models import Post, MyUser


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content_html', 'status']


class UsrForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content_html']
