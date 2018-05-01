from django.shortcuts import render
from django.http import HttpResponse
from django .template import loader


# Create your views here.

def home(request):  # this is just a test make sure to try this path first to make sure that everything is ok
    return render(request, 'Social_Network/test.html')


