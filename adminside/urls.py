from django.urls import path
from . import views
from .views import *


urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_mangement/', views.user_mangement, name='user_mangement'),
    path('user_block/<int:user_id>/', views.user_block, name='user_block'),
    path('sales_report/',views.sales_report,name='sales_report'),
    path('export_csv/',views.export_csv,name='export_csv'),
    path('generate_pdf/',views.generate_pdf,name='generate_pdf'),





    
]