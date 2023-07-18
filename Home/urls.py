from django .contrib import admin
from django.urls import path,include
from .import views
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('shop/',shop,name="shop"),
    
]
