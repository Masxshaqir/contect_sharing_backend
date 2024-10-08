from django.db import models
import uuid
from accounts.models import User

    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title =models.CharField(max_length=50,null=False,blank=False)
    category =models.CharField(max_length=50,null=False,blank=False , choices=(('Entertaining','Entertaining') ,
                                                                                 ('Motivational','Motivational'),
                                                                                 ('Emotional','Emotional'),
                                                                                 ('Sadness','Sadness'),
                                                                                 ('Thought-Provoking','Thought-Provoking'),
                                                                                 ('Romantic','Romantic')))
    hashtag=models.CharField(max_length=150,null=False,blank=False)
    content=models.CharField(max_length=500,null=True,blank=True)
    post_image=models.FileField(upload_to='static/Posts/',null=True,blank=True)
    post_time=models.DateTimeField(auto_now_add=True)
    post_update_time=models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.email} Post {self.title}"
        
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    comment =models.CharField(max_length=500,null=False,blank=False)
    comment_time=models.DateTimeField(auto_now_add=True)
    comment_update_time=models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} Comment on  {self.post.title}"
    
class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vote=models.IntegerField(null=False,blank=False,choices=((1,1),(2,2),(3,3),(4,4),(5,5)))
    vote_time=models.DateTimeField(auto_now_add=True)
    vote_update_time=models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'post') 
    def __str__(self):
        return f"{self.user.email} Rate on  {self.post.title}"
    