from django.shortcuts import render
from django .http import HttpResponsePermanentRedirect
from .forms import postForm
from django.http import HttpResponse
from django .template import loader
from .models import *


# Create your views here.

def home(request): # news feed and posts from other freaks

    if request.method == 'POST':
        user_of_post = User.objects.get(id =request.user.id)

        # Create a form instance
        form = postForm(request.POST)
        if(form.is_valid()):
            post_of_user = form.cleaned_data
            post = Post(publisher=user_of_post , content=post_of_user)
            post.save()




    else:
        form = postForm()

    return render(request,'Social_Network/test.html',{'form' : form })