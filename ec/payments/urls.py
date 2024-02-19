# urls.py

from django.urls import path
from . import views

urlpatterns = [
    
    path('add_payment_method/', views.add_payment_method, name='add_payment_method'),
    path('process_payment/', views.process_payment, name='process_payment'),
    
    


    # Add more URL patterns as needed
]