from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [

    path('login/', views.loginPage, name="login_page"),
    path('register/', views.registerPage, name="register_page"),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('delete_part/<int:pk>/', views.deletePart, name="delete_part"),
    path('', views.part_list, name="part_list"),
    path('part_create/', views.part_create, name="part_create"),
    path('assembly_create/', views.assembly_create, name="assembly_create"),
    path('assembly_list/', views.assembly_list, name="assembly_list"),
    
]
