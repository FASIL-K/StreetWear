from django.urls import path
from .import views

urlpatterns = [
    path('product_detalis/<int:product_id>/',views.single, name='product_detalis'),
    path('shop/',views.shop,name="shop"),

    
]
