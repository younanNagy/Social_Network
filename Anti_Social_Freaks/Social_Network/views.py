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

def getSuggestedFriends(id):
    my_connections = Connection.objects.filter(From=id ,status=1)#bagib el friends bto3i

    suggested_friends=[]
    suggested_connections=[]


    for connection in my_connections:
        suggested_connections.append( Connection.objects.filter(From=connection.To, status=1))

    for connection in suggested_connections:
        if connection.To!=id :
            suggested_friends.append(connection.To)

    return suggested_friends




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
        search_form = searchForm()

    comment_form = commentForm()
    posts = Post.objects.exclude(publisher=request.user)

   # suggested_friends=getSuggestedFriends(request.user)

    context = {
        'user': request.user,
        'post_form': post_form,
        'comment_form': comment_form,
        'posts': posts,
        'search_form' : search_form,
    #    'suggested_friends' : suggested_friends
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




def search(request):
    search_form = searchForm(request.POST)
    user_of_search = User.objects.get(id=request.user.id)
    if (search_form.is_valid()):
        username = search_form.cleaned_data['username']
        user_of_search = User.objects.get(username=username)

    context = {'username' : user_of_search}
    return render(request, 'Social_Network/profile.html',context)


def addFriend(request,friend_id):
    user_from = User.objects.get(id=request.user.id)
    user_to   = User.objects.get(id=friend_id)

    test_connection = Connection.objects.filter(From= user_from , To= user_to)

    if(test_connection.exists()):
        test_connection = test_connection[0]
        test_connection.status = 0
        test_connection.save()

    else:
        connection = Connection(From=user_from,To=user_to,status=0,interaction=0)
        connection.save()

    return redirect('home')

def unFriend(request,friend_id):
    user_from = User.objects.get(id=request.user.id)
    user_to   = User.objects.get(id=friend_id)

    test_connection = Connection.objects.filter(From= user_from , To= user_to)

    if(test_connection.exists()):
        connection1 = test_connection[0]
        connection1.delete()

    test_connection2 = Connection.objects.filter(From=user_to, To=user_from)

    if (test_connection2.exists()):
        connection2 = test_connection2[0]
        connection2.delete()


    return redirect('home')


def followFriend(request,friend_id):
    user_from = User.objects.get(id=request.user.id)
    user_to   = User.objects.get(id=friend_id)

    test_connection = Connection.objects.filter(From= user_from , To= user_to)

    if(test_connection.exists()):
        test_connection = test_connection[0]
        test_connection.status = 4
        test_connection.save()

    else:
        connection = Connection(From=user_from,To=user_to,status=4,interaction=0)
        connection.save()

    return redirect('home')




def confirmFriend(request,friend_id):
    user_to = User.objects.get(id=request.user.id)
    user_from   = User.objects.get(id=friend_id)

    test_connection = Connection.objects.filter(From= user_from , To= user_to)

    if(test_connection.exists()):# must exist
        test_connection = test_connection[0]
        test_connection.status = 1
        test_connection.save()
    #cheking reverse connection
    test_connection = Connection.objects.filter(From=user_to, To=user_from)

    # el goz2  da 34an lw A---->(add)B && B------>(follw)A
    if (test_connection.exists()):#may not exist
        test_connection = test_connection[0]
        test_connection.status = 1
        test_connection.save()
    else:
        connection = Connection(From=user_to,To=user_from,status=1,interaction=0)# creating reverse connection
        connection.save()

    return redirect('home')


def showRequest(request):

    friend_requests=Connection.objects.filter(To=request.user,status=0)
    context={
        'friend_requests' : friend_requests
    }
    return render(request, 'Social_Network/Friend_requests.html', context)