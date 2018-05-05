from django.shortcuts import render
from django .http import HttpResponsePermanentRedirect
from .forms import *
from django.http import HttpResponse
from django .template import loader
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import logout

# Create your views here.




####################### Log In and Log Out




def register(request):
    if request.method =='POST':

        form = RegistrationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/anti-social/login')
    else:
        form= RegistrationForm()

        args={'form':form}
        return render(request,'Social_Network/registration.html',args)





def login_redirect( request ):
    return redirect("/anti-social/home")





def logout_view(request):
    logout(request)
    return render(request,'Social_Network/logout.html')




####################### Log In and Log Out





def home(request): # news feed and posts from other freaks

    if request.method == 'POST':
        # Create a form instance
        post_form = postForm(request.POST)


        if(post_form.is_valid()):
            user_of_post = User.objects.get(id=request.user.id)
            post_of_user = post_form.cleaned_data['post']
            post = Post(publisher=user_of_post , content=post_of_user)
            post.save()



    else:
        post_form = postForm()

    comment_form = commentForm()
    posts = Post.objects.exclude(publisher=request.user)
    context = {
        'post_form': post_form,
        'comment_form': comment_form,
        'posts': posts
    }

    return render(request, 'Social_Network/home.html', context)


def addComment(request,post_id):
    comment_form = commentForm(request.POST)

    if (comment_form.is_valid()):
        user_of_comment = User.objects.get(id=request.user.id)
        post_of_comment = Post.objects.get(id=post_id)
        comment_of_post = comment_form.cleaned_data['comment']
        comment = Comment(post=post_of_comment,content=comment_of_post,commenter=user_of_comment)
        comment.save()

    return redirect('home')




def addLike(request,post_id):

    user_of_like = User.objects.get(id=request.user.id)
    post_of_like = Post.objects.get(id=post_id)
    like = Like(post=post_of_like,liker=user_of_like)
    like.save()
    return redirect('home')

