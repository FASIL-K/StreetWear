from django.urls import path
from .import views

urlpatterns = [
    path('checkout/',views.checkout, name='checkout'),
    path('placeorder/',views.placeorder, name='placeorder'),
    path('addcheckoutaddr/',views.addcheckoutaddr, name='addcheckoutaddr'),
    path('deleteaddresscheckout/<int:delete_id>/',views.deleteaddresscheckout, name='deleteaddresscheckout'),
    path('razarypaycheck/',views.razarypaycheck, name='razarypaycheck'),


]