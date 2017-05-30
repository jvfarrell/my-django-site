"""mysite URL Configuration

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
from mysite.views import hello, my_homepage_view, current_datetime, hours_ahead, display_meta, contact, resume, home, nfl_analytics
from books import views
from lol import views as lolview

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home),
    url(r'^hello/$', hello),
    url(r'^resume/$', resume),
    url(r'^home/$', home),
    url(r'^nfl/$', nfl_analytics),
    url(r'^time/$', current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^MetaDisplay/', display_meta),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),
    url(r'^lolsearch/$', lolview.search),
    url(r'^summoner/(.*)/$', lolview.summoner),
    url(r'^summoner/$', lolview.summoner_landing),
    url(r'^contact/$', contact),
]
