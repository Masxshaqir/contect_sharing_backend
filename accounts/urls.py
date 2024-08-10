from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/', register , name="register"),
    path('login/', signin , name="login"),
    path('logout/', Logout , name="logout"),
    path('get_profile/', get_profile , name="get_profile"),
    path('add_friend/', add_friend , name="add_friend"),
    path('get_all_users/', get_all_users , name="get_all_users"),
    path('get_following_users/', get_following_users , name="get_following_users"),
    path('update_profile/', update_profile , name="update_profile"),
]