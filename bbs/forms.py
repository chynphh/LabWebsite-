from django import forms
from .models import Post, MyUser, Reply, Comment, Martor
from martor.fields import MartorFormField


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content_html', 'status']


class UserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['name', 'avatar']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content_html']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class SimpleForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    description = MartorFormField()
    wiki = MartorFormField()


class MartorForm(forms.ModelForm):

    class Meta:
        model = Martor
        fields = '__all__'