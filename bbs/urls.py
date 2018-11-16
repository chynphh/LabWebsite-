from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'login', views.my_login, name='login'),
    path(r'login_func', views.login_func, name='login_func'),
    path(r'logout_func', views.logout_func, name='logout_func'),
    path(r'add_post', views.add_post, name='add_post'),
    path(r'', views.index, name='index'),
    path(r'index', views.index, name='index'),
    path(r'test', views.test, name='test'),
    re_path(r'detail/(?P<pk>\d+)', views.detail, name='detail'),
    re_path(r'add_reply/(?P<pk>\d+)', views.add_reply, name='add_reply'),
    re_path(r'add_comment/(?P<reply_pk>\d+)/(?P<user_to_pk>\d+)', views.add_comment, name='add_comment'),

]
