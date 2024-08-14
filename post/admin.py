from django.contrib import admin

from post.models import *

# Register your models here.
      
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Post)
