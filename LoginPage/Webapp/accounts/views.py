from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'accounts/dashboard.html')

def helpPage(request):
    return render(request, 'accounts/help.html')

def aboutPage(request):
    return render(request, 'accounts/about.html')

def myProjects(request):
    return render(request, 'accounts/myprojects.html')