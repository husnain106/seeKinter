from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home),
    path('myprojects/', views.myProjects),
    # path('help/', views.helpPage, name="help"),
    path('about/', views.aboutPage, name="about"),
    path('login/', views.login, name = "login/"),
    path('signup/', views.signup, name = "signup/"),
    path('logout/', views.logout, name="logout"),
    path('myprojects/project_saved/<str:param>',views.file),
    path('project/', views.widgets),
    path('myprojects/delete-project/<str:param>', views.delete_project),
    path('myprojects/duplicate-project/<str:param>', views.duplicate_project),
] 


urlpatterns += staticfiles_urlpatterns()