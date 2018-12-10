#coding:utf-8
"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from article import views
from article.views import RSSFeed
from pages import views as pages_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    # url(r'^(?P<my_args>\d+)/$', views.detail1, name='detail'),
    url(r'^id/(?P<id>\d+)/$', views.detail2, name='detai2'),
    url(r'^lover/$', pages_views.display, name = "love"),
    url(r'^bookmarks/$', pages_views.bookmarks, name = "bookmarks"),
    url(r'^test/$', views.test),
    url(r'^output/$', views.output),
    url(r'^tag/(?P<tag>\w+)/$', views.search_tag, name = 'search_tag'),
    url(r'^feed/$', RSSFeed(), name = "RSS"),
    url(r'^qq/$', pages_views.qq, name = "qq"),
    url(r'^ccc/$', pages_views.qq, name = "qq"),
    url(r'^999/$', pages_views.qq, name = "qq"),
    url(r'^666/$', pages_views.qq, name = "qq"),
    url(r'^news/$', pages_views.qq, name = "qq"),
    url(r'^photos/$', pages_views.qq, name = "qq"),

]
