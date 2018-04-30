from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request): # this is just a test make sure to try this path first to make sure that everyting is ok
    return HttpResponse("<h1> Home Page")