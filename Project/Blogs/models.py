from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Blogger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='blogger')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="profile_pictures/",null=True,blank=True)
    interests = models.TextField(null=True, blank=True)
    qualities = models.TextField(null=True, blank=True)
    proffession = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Blogger, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField()
    date_last_edit = models.DateTimeField()
    files = models.FileField(upload_to="images/")

    def __str__(self):
        return self.title + " " + self.author.first_name + " " + self.author.last_name


class Comment(models.Model):
    content = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content + " " + self.blogger.first_name + " " + self.blogger.last_name


class BloggerBlockedUser(models.Model):
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE, null=True, blank=True,related_name='blogger_blocker')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='blogger_blocked')