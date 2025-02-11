from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('parts', views.getParts),
    path('assemblies', views.getAssemblies),
]
