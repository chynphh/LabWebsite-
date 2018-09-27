"""pku_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# from django.conf.urls import url
from web import views as web_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', web_views.home, name='home'),
    path(r'about', web_views.about, name='about'),
    path(r'publication', web_views.publication, name='publication'),
    path(r'team', web_views.team, name='team'),
    path(r'research', web_views.research, name='research'),
    path(r'news', web_views.news, name='news'),
    path(r'test/', web_views.test, name='test'),
    path(r'base/', web_views.base, name='base'),
    re_path(r'detial/(?P<detialtype>[a-z]*)/(?P<pk>[0-9]*)', web_views.detial, name='detial'),
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

