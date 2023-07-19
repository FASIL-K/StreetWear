from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('product_management/',views.product_management,name="product_management"),
    path('delete_product/<int:prod_id>/',views.delete_product,name="delete_product"),
    path('add_product/',views.add_product,name="add_product"),

    
]
