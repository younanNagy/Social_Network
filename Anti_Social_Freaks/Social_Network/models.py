from django.db import models
from django.contrib.auth.models import User
from datetime import datetime





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


class Connection(models.Model):
    From = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    To = models.ForeignKey(User, on_delete=models.CASCADE)
    interaction = models.IntegerField(blank=True)  # indicates how much a user interacts with another
    status = models.IntegerField()

    def __str__(self):
        if (self.status == 0):
            return '%s' % ("Pending")


        elif (self.status == 1):
            return '%s %s %s' % ("Friends" , self.From.username, self.To.username)


        elif (self.status == 2):
            return '%s' % ("Declined")

        elif (self.status == 3):
            return '%s' % ("Blocked")


        elif (self.status == 4):
            return '%s' % ("Followed")

        else:
            return '%s' % ("Blocked")

    '''
    status code
    pending : 0
    Friends : 1
    Declined : 2
    Blocked : 3
    Follow :4
    '''


