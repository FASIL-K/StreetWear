"""
URL configuration for Street_wear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django .conf .urls .static import static
from django .conf import settings
from django.contrib.auth import views as auth_views
from account import views
from Home import views
from Home import views as home_views  # Import the home view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Home.urls')),
    path('',include('account.urls')),
    path('',include('adminside.urls')),
    path('',include('category.urls')),
    path('',include('products.urls')),
    path('',include('shop.urls')),
    path('',include('cart.urls')),
    path('',include('checkout.urls')),
    path('',include('userprofile.urls')),
    path('',include('orders.urls')),
    path('',include('wishlist.urls')),
    path('',include('coupon.urls')),
    path('',include('banner.urls')),
    path('',include('offer.urls')),


    path('login/', views.custom_login, name='custom_login'),  # Custom login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', home_views.home, name='home'),  # Home view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

