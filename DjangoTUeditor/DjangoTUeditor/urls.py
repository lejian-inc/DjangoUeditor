#coding=utf-8
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
import views

urlpatterns = [ 
    url(r"^controller/$", views.action_controller),
]



