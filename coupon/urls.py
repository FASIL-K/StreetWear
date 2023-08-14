from django.urls import path
from .import views
urlpatterns = [
   
   path('coupons/',views.coupons,name='coupons'),
   path('addcoupons/',views.addcoupons,name='addcoupons'),
   path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
   path('remove_coupon/',views.remove_coupon,name='remove_coupon'),

]