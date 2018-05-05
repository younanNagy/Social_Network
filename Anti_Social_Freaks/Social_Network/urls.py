from django .urls import path
from . import views
from django.contrib.auth.views import login,logout


# all add your needed urls here
urlpatterns = [



    # Sign Up, Log in and Log out
    # this is just a test make sure to try this path first to make sure that everyting is ok
    path('login/', login, {'template_name': 'Social_Network/login.html'}),
    path('logout/', logout, {'template_name': 'Social_Network/logout.html'}),
    path('register/', views.register, name='register'),


    path('home',views.home , name='home'), # home page
    path('CommentPost/<int:post_id>/', views.addComment, name='addcomment'), # add a comment for a given post id
    path('LikePost/<int:post_id>/', views.addLike, name='addLike'), # add a Like for a given post id
    path('searchUser',views.search,name='search'), # Search for a user and go to it's profile
    path('AddFriend/<int:friend_id>/',views.addFriend,name='addfriend'),
    path('FollowFriend/<int:friend_id>/', views.followFriend, name='followfriend'),
    path('unFriend/<int:friend_id>/', views.unFriend, name='unfriend' ),
    path('FriendRequests/', views.showRequest, name='showrequest' ),
    path('FriendRequests/Confirm/<int:friend_id>/', views.confirmFriend, name='confirmfriend'),

]