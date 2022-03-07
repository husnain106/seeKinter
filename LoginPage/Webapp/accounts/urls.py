from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.home),
    path('myprojects/', views.myProjects),

    path('help/', views.helpPage, name="help"),
    path('about/', views.aboutPage, name="about"),
    path('login/', views.login, name = "login/"),
    path('signup/', views.signup, name = "signup/")
] 

urlpatterns += staticfiles_urlpatterns()