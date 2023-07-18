from django.urls import path
from . import views
from .views import *


urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_mangement/', views.user_mangement, name='user_mangement'),
    path('user_block/<int:user_id>/', views.user_block, name='user_block'),




    
]