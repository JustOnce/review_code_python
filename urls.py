from django.urls import path 
from . import views

urlpatterns = [
    path('', views.TransferView.as_view()),
]