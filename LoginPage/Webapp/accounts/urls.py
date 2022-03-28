from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home),
    path('myprojects/', views.myProjects),
    path('help/', views.helpPage, name="help"),
    path('about/', views.aboutPage, name="about"),
    path('login/', views.login, name = "login/"),
    path('signup/', views.signup, name = "signup/"),
    path('logout/', views.logout, name="logout"),
    re_path('^myprojects/file/(\w)',views.file),
    path('project/', views.widgets),
    re_path('^myprojects/delete-project/(\w)', views.delete_project),
    re_path('^myprojects/duplicate-project/(\w)', views.duplicate_project)
] 


urlpatterns += staticfiles_urlpatterns()