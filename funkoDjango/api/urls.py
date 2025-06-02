from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllFunkos),
    path('getItem', views.getItem)
]
