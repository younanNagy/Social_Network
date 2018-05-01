from django.db import models
from django.contrib.auth.models import User


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
    date_of_post = models.DateTimeField(null=True)

    def __str__(self):
        return self.content
2

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE ,null=True )

    def __str__(self):
        return self.content


class Like(models.Model):
    liker=models.ForeignKey(User,on_delete=models.CASCADE)
    # Type of Like is missing
    post=models.ForeignKey(Post, on_delete=models.CASCADE)


class Connection(models.Model):
    From = models.ForeignKey(User, on_delete=models.CASCADE)
    To = models.CharField(max_length=50)
    interaction = models.IntegerField() # indicates how much a user interacts with another
    status = models.IntegerField()
    '''
    status code
    pending : 0
    Friends : 1
    Declined : 2
    Blocked : 3
    

    def __str__(self):
        if (status == 0):
            return "pending"
        elif (status == 1):
            return "Friends"
        elif (status == 2):
            return "Declined"
        else :
            return "Blocked"
    '''






