# urls.py

from django.urls import path
from . import views

urlpatterns = [
    
    path('add_payment_method/', views.add_payment_method, name='add_payment_method'),

    # Add more URL patterns as needed
]