"""mongodb_backup URL Configuration

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
from django.urls import path
from django.conf.urls import url
from backup_web.views import index,web_mongo,web_mongo_elk,chart_data,web_mongo_allweb,web_mongo_zabbix,web_mongo_guanwu,web_mongo_pike,web_mongo_redmine,web_mongo_db

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^index/', index),
    url('^web_mongo/', web_mongo),
    url('^web_mongo_elk/', web_mongo_elk),
    url('^web_mongo_allweb/', web_mongo_allweb),
    url('^web_mongo_zabbix/', web_mongo_zabbix),
    url('^web_mongo_guanwu/', web_mongo_guanwu),
    url('^web_mongo_pike/', web_mongo_pike),
    url('^web_mongo_redmine/', web_mongo_redmine),
    url('^web_mongo_db/', web_mongo_db),
    url('^chart_data/', chart_data),
]
