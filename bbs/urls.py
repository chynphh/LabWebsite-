from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'login', views.my_login, name='login'),
    path(r'login_func', views.login_func, name='login_func'),
    path(r'logout_func', views.logout_func, name='logout_func'),
    path(r'index', views.index, name='index'),
    path(r'test', views.test, name='test'),

]
