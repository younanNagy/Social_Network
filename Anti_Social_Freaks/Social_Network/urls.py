from django .urls import path
from . import views



# all add your needed urls here
urlpatterns = [
    path('',views.home , name='home') # this is just a test make sure to try this path first to make sure that everyting is ok
]