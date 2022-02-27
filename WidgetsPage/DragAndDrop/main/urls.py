from django.urls import path
from . import views


urlpatterns = [path('', views.main), path('dd/', views.render_dd)]