from django.urls import path
from .import views

urlpatterns = [
    path('orders/',views.orders, name='orders'),
    path('vieworderdetail/<int:orderitem_id>/',views.vieworderdetail, name='vieworderdetail'),
    path('order_management/',views.order_management, name='order_management'),
    path('orderdetails_admin/<int:track_id>/',views.orderdetails_admin, name='orderdetails_admin'),
    path('changestatus',views.changestatus, name='changestatus'),
    path('ordercancel',views.ordercancel, name='ordercancel'),
    path('orderreturn/<int:return_id>/',views.orderreturn, name='orderreturn'),

  
]