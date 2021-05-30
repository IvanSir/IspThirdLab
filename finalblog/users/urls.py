from django.contrib import admin
from django.urls import path
from .views import register, my_login, my_logout, UserDetailView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', my_login, name='login'),
    path('logout/', my_logout, name='logout'),
    path('<pk>', UserDetailView.as_view(), name='detail_user')
]