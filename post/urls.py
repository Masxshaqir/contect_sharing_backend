from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
  
    path('add_post/', add_post , name="add_post"),
    path('get_all_posts/', get_all_posts , name="get_all_posts"),
    path('update_post/', update_post , name="update_post"),
]