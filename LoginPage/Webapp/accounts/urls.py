from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),

    path('', views.home),
    

    path('help/', views.helpPage, name="help"),
    path('about/', views.aboutPage, name="about"),

]