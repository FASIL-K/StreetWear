from django.urls import path
from .import views
urlpatterns = [
 
 path('offer/',views.offer,name='offer'),
 path('add_offer/',views.add_offer,name='add_offer'),
#  path('offer_search/',views.offer_search,name='offer_search'),
 path('edit_offer/<int:offer_id>',views.edit_offer,name='edit_offer'),
 path('delete_offer/<int:delete_id>',views.delete_offer,name='delete_offer'),
  path('offer_search/',views.offer_search,name='offer_search'),

  
]