from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('', views.home, name='home'),
    
    path('', include('item.urls')),
    path('', include('location.urls')),
    path('', include('inventory.urls')),
    path('', include('inflow.urls')),
    path('', include('outflow.urls')),
    path('', include('order.urls')),

]
