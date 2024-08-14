from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
  
    path('add_post/', add_post , name="add_post"),
    path('get_all_posts/', get_all_posts , name="get_all_posts"),
    path('update_post/', update_post , name="update_post"),
    path('add_comment/', add_comment , name="add_comment"),
    path('update_comment/', update_comment , name="update_comment"),
    path('delete_comment/', delete_comment , name="delete_comment"),
    path('add_vote/', add_vote , name="add_vote"),
    path('update_vote/', update_vote , name="update_vote"),
    path('get_votes/', get_votes , name="get_votes"),
]