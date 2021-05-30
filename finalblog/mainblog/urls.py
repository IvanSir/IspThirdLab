from django.contrib import admin
from django.urls import path, include

from mainblog.views import HomeView, create_post, DetailPostView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', create_post, name='create_post'),
    path('post/<slug:slug>', DetailPostView.as_view(), name='detail_post')
]