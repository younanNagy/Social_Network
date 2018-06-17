from django.shortcuts import render
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import logout
from collections import defaultdict

# Create your views here.


def start(request):
    return render(request,'Social_Network/start.html')




####################### Log In and Log Out

def NewsFeed(id):
    current_user = User.objects.get(id=id)
    my_connections = Connection.objects.filter(From=current_user, status=1)
    time_line_posts=[]
    for connection in my_connections:
        friend=User.objects.get(id=connection.To.id)
        friend_post=Post.objects.filter(publisher=friend).order_by('-date')
        time_line_posts.extend(friend_post)


    return time_line_posts



def is_friend(myid,friend_id):
    current_user=User.objects.get(id=myid)
    friend=User.objects.get(id=friend_id)

    my_connections = Connection.objects.filter(From=current_user, status=1)
    for connection in my_connections:
        if(connection.To.id==friend.id):
            return True

    return False


def getSuggestedFriends(id):
    current_user= User.objects.get(id=id)
    my_connections = Connection.objects.filter(From=current_user, status=1)  # bagib el friends bto3i
    suggested_friends = []
    suggested_connections = []

    suggested_friends_dict=defaultdict(int)

    for connection in my_connections:
        friend = User.objects.get(id=connection.To.id)
        suggested_connections.extend(Connection.objects.filter(From=friend, status=1))

    for suggested_connection in suggested_connections:
        suggested_friend = User.objects.get(id=suggested_connection.To.id)
        if suggested_friend.id != current_user.id:
            suggested_friends_dict[suggested_friend] = suggested_friends_dict[suggested_friend]+1
           # suggested_friends.append(suggested_friend)

    for suggested_friend in suggested_friends_dict:
        if((suggested_friends_dict[suggested_friend]>=2) and not (is_friend(id,suggested_friend.id))):
            suggested_friends.append(suggested_friend)

    return suggested_friends


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

    search_form = searchForm()
    comment_form = commentForm()
    posts = NewsFeed(request.user.id)
    suggested_friends = getSuggestedFriends(request.user.id)
    context = {
        'user': request.user,
        'post_form': post_form,
        'comment_form': comment_form,
        'posts': posts,
        'search_form' : search_form,
        'suggested_friends' : suggested_friends
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

    return redirect('Social_Network:home')

def addLike(request,post_id):
    user_of_like = User.objects.get(id=request.user.id)
    post_of_like = Post.objects.get(id=post_id)
    like = Like(post=post_of_like,liker=user_of_like)
    like.save()
    return redirect('Social_Network:home')

def search(request):
    search_form = searchForm(request.POST)
    user_of_search = User.objects.get(id=request.user.id)
    if (search_form.is_valid()):
        username = search_form.cleaned_data['username']
        user_of_search = User.objects.get(username=username)

    posts = Post.objects.filter(publisher=user_of_search)
    context = {'username' : user_of_search , 'posts' :posts}
    return render(request, 'Social_Network/profile.html',context)



def profile(request):
    user = User.objects.get(id = request.user.id)
    posts = Post.objects.filter(publisher=user).order_by('-date')
    friend_requests=Connection.objects.filter(To=request.user,status=0)
    context = {'profile' : user , 'posts':posts , 'friend_requests' : friend_requests}
    return render(request,'Social_Network/myprofile.html',context)


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

    return redirect('Social_Network:home')

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


    return redirect('Social_Network:home')

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

    return redirect('Social_Network:home')

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

    return redirect('Social_Network:home')

def showRequest(request):

    friend_requests=Connection.objects.filter(To=request.user,status=0)
    context={
        'friend_requests' : friend_requests
    }
    return render(request, 'Social_Network/Friend_requests.html', context)



def userProfile(request,user_id):

    user = User.objects.get(id = user_id)
    posts = Post.objects.filter(publisher=user)
    context = {'username': user , 'posts' : posts}
    return render(request, 'Social_Network/profile.html', context)


######################### Graph

def generate_graph(graph):
    graph_connections = Connection.objects.filter(status=1)

    for connection in graph_connections:
        graph.add_edge(connection.From.id, connection.To.id)




class Graph:
    # Constructor
    def __init__(self):
        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.visited = defaultdict(bool)
        self.adj_matrix = defaultdict(list)

    #function to add edges
    def add_edge(self, u, v):
        self.graph[str(u)].append(str(v))
        user_from = User.objects.get(id=u)
        user_to = User.objects.get(id=v)
        self.adj_matrix[user_from.username].append(user_to.username)

    #v is the starting node and u is the node we are trying to find a connection between it and v
    def explore(self,v, u, connected):
        print(v)
        self.visited[str(v)] = True
        if str(v) == str(u):
            connected =True

        for i in self.graph[str(v)]:
            if self.visited[i] == False:
                connected = self.explore(i, u, connected)

        return connected



    def DFS(self, v, u):

        connected =False
        for i in self.graph:
            self.visited[i] = False



        return self.explore(v, u, connected)





def checkConnection(request,user_id):
    user_to = User.objects.get(id=user_id)
    user_from = User.objects.get(id = request.user.id)
    g = Graph()
    generate_graph(g)
    connection = g.DFS(user_from.id,user_to.id)
    print(g.adj_matrix)
    adj_matrix = g.adj_matrix

    graph_string = []


    for y in adj_matrix:
        s = y
        s = s + ' -> '
        for x in adj_matrix[y]:
            s = s + x
            s = s + ', '

        s = s[:-2]
        graph_string.append(s)

    context = { 'connection' : connection , 'adj_matrix' : graph_string}
    return render(request,'Social_Network/connection.html',context)



