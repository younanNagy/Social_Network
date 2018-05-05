from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
    mobile=models.CharField(max_length=11)
    about=models.CharField(max_length=500)
    date_of_birth= models.DateField()
    image=models.ImageField(upload_to='profile_image',blank=True)#$$$$$$$$$$$$$$$$$

    def __str__(self):
        return self.user.username



class Post(models.Model):# shares is missing $$$$$$$$$$
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    date = models.DateTimeField(blank=True,default=datetime.now)

    def __str__(self):
        return self.content


class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE ,null=True )

    def __str__(self):
        return self.content


class Like(models.Model):
    liker=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.liker, 'Liked', self.post)






