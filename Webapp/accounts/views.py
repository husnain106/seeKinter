from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout


def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # if user is not None:
        #     login(request, user)
        #     redirect('home')
        # else:
        #     pass

    context = {}
    return render(request, 'accounts/login.html', context)

def home(request):
    return render(request, 'accounts/dashboard.html')

def products(request):
    return render(request, 'accounts/products.html')

def customer(request):
    return render(request, 'accounts/customer.html')