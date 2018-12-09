from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'login', views.my_login, name='login'),
    path(r'login_func', views.login_func, name='login_func'),
    path(r'logout_func', views.logout_func, name='logout_func'),
    path(r'add_post', views.add_post, name='add_post'),
    path(r'', views.index, name='index'),
    path(r'index', views.index, name='index'),
    path(r'profile', views.profile, name='profile'),
    re_path(r'detail/(?P<pk>\d+)', views.detail, name='detail'),
    re_path(r'add_reply/(?P<pk>\d+)', views.add_reply, name='add_reply'),
    re_path(r'add_comment/(?P<reply_pk>\d+)/', views.add_comment, name='add_comment'),
    path(r'upload', views.upload, name='upload'),
    re_path(r'delete/(?P<delete_type>[a-z]*)/(?P<pk>\d+)', views.delete, name='delete'),
    path(r'user_mark_all_read', views.user_mark_all_read, name='user_mark_all_read'),
    re_path(r'api/uploader/$', views.markdown_uploader, name='markdown_uploader_page'),

    path(r'test', views.test, name='test'),
    path(r'test_post', views.test_post, name='test_post'),

]
