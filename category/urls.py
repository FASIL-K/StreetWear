from django.urls import path
from . import views
from .views import *


urlpatterns = [
    
    path('category_management/', views.category_management, name='category_management'),
    # path('add_category/', views.add_category, name='add_category'),
    # path('edit_category/ <int:category_id>', views.edit_category, name='edit_category'),
    path('delete_category/ <int:category_id>', views.delete_category, name='delete_category'),
    path('brand_management/', views.brand_management, name='brand_management'),    
    path('add_brand/', views.add_brand, name='add_brand'),
    path('edit_brand/<int:brand_id>', views.edit_brand, name='edit_brand'),
    path('delete_brand/<int:brand_id>', views.delete_brand, name='delete_brand'),

]