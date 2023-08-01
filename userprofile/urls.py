from django.urls import path
from .import views

urlpatterns = [
    path('userprofile/',views.userprofile, name='userprofile'),
    path('addaddress/',views.addaddress, name='addaddress'),
    path('editprofiles/', views.editprofiles, name='editprofiles'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('deleteaddress/<int:delete_id>', views.deleteaddress, name='deleteaddress'),


]