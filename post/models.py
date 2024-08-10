from django.db import models

from accounts.models import User

    
class Post(models.Model):
    title =models.CharField(max_length=50,null=False,blank=False)
    category =models.CharField(max_length=50,null=False,blank=False , choices=(('Entertaining','Entertaining') ,
                                                                                 ('Motivational','Motivational'),
                                                                                 ('Emotional','Emotional'),
                                                                                 ('Sadness','Sadness'),
                                                                                 ('Thought-Provoking','Thought-Provoking'),
                                                                                 ('Romantic','Romantic')))
    hashtag=models.CharField(max_length=150,null=False,blank=False)
    contect=models.CharField(max_length=500,null=False,blank=False)
    post_image=models.FileField(upload_to='static/Posts/',null=False,blank=False)
    post_time=models.DateTimeField(auto_now_add=True)
    post_update_time=models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.email} Post {self.title}"