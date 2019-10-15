"""example URL Configuration

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

from django_grapesjs.views.admin import GetTemplate

from app.views import (
    GrapesJSTemplateView, GrapesJSDetailView,
    GrapesJSCreateView, GrapesJSDeleteView,
    GrapesJSListView,
    GrapesJSLoadView, GrapesJSUpdateView
)


try:
    from django.urls import re_path

    urlpatterns = [
        re_path('^admin/', admin.site.urls),
        re_path('^template/list/$', GrapesJSListView.as_view(), name='template-list'),
        re_path('^template/create/', GrapesJSCreateView.as_view(), name='template-create'),
        re_path('^template/(?P<pk>\d+)/?$', GrapesJSDetailView.as_view(), name='template'),
        re_path('^template/load/(?P<pk>\d+)/?$', GrapesJSLoadView.as_view(), name='template-load'),
        re_path('^template/save/(?P<pk>\d+)/?$', GrapesJSUpdateView.as_view(), name='template-save'),
        re_path('^template/delete/(?P<pk>\d+)/?$', GrapesJSDeleteView.as_view(), name='template-delete'),
        # Admin
        re_path('^get_template/$', GetTemplate.as_view(), name='dgjs_get_template'),

    ]

except ImportError:
    from django.conf.urls import include, url

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url('^template/list/$', GrapesJSListView.as_view(), name='template-list'),
        url('^template/create/', GrapesJSCreateView.as_view(), name='template-create'),
        url('^template/(?P<pk>\d+)/?$', GrapesJSDetailView.as_view(), name='template'),
        url('^template/load/(?P<pk>\d+)/?$', GrapesJSLoadView.as_view(), name='template-load'),
        url('^template/save/(?P<pk>\d+)/?$', GrapesJSUpdateView.as_view(), name='template-save'),
        url('^template/delete/(?P<pk>\d+)/?$', GrapesJSDeleteView.as_view(), name='template-delete'),
        url('^get_template/$', GetTemplate.as_view(), name='dgjs_get_template'),
    ]
