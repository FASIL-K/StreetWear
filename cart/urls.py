from django.urls import path
from .import views

urlpatterns = [
    path('cart/',views.cart, name='cart'),
    path('addtocart',views.addtocart, name='addtocart'),
    path('deletecartitem/<int:id>', views.deletecartitem, name='deletecartitem'),
    path('update_cart/', views.update_cart, name='update_cart'),

]
