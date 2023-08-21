from django.urls import path
from .import views

urlpatterns = [
    path('banner/',views.banner, name='banner'),
    path('createbanner/',views.createbanner, name='createbanner'),
    path('editbanner/<int:banner_id>/', views.editbanner, name='editbanner'),
    path('deletebanner/<int:banner_id>/', views.deletebanner, name='deletebanner'),

  
]