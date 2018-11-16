from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'about', views.about, name='about'),
    path(r'publication', views.publication, name='publication'),
    path(r'team', views.team, name='team'),
    path(r'research', views.research, name='research'),
    path(r'news', views.news, name='news'),
    re_path(r'detail/(?P<detailtype>[a-z]*)/(?P<pk>[0-9]*)', views.detail, name='detail'),

]
