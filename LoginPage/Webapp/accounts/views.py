from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout


def registerPage(request):
    # form = UserCreationForm()
    # context = {'form': form}
    return render(request, 'accounts/register.html')


def loginPage(request):
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')

    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         redirect('home')
    #     else:
    #         pass

    # context = {}
    return render(request, 'accounts/login.html')


def home(request):
    return render(request, 'accounts/dashboard.html')

def helpPage(request):
    return render(request, 'accounts/help.html')

def aboutPage(request):
    return render(request, 'accounts/about.html')