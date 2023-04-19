from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=255,null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    author = models.ForeignKey(User,on_delete= models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.title)

