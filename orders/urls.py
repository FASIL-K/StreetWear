from django.urls import path
from .import views

urlpatterns = [
    path('orders/',views.orders, name='orders'),
    path('vieworderdetail/<int:orderitem_id>/',views.vieworderdetail, name='vieworderdetail'),
  
]