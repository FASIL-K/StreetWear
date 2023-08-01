from django .contrib import admin
from django.urls import path,include
from .import views
from .views import *

urlpatterns = [
    path('signin/',signin,name="signin"),
    path('signup/',signup,name="signup") ,
    path('signout/',signout,name="signout"),
    path('admin_login/',admin_login,name="admin_login"),
    path('admin_logout/',admin_logout,name="admin_logout"),
    path('forgot_password',views.forgot_password,name='forgot_password'),




    
]
