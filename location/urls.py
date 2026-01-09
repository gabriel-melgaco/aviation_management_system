from django.urls import path
from . import views


urlpatterns = [
    path('location/list/', views.LocationListView.as_view(), name='location_list'),
    path('location/create/', views.LocationCreateView.as_view(), name='location_create'),
    path('location/<int:pk>/details/', views.LocationDetailView.as_view(), name='location_detail'),
    path('locaiton;<int:pk>/update/', views.LocationUpdateView.as_view(), name='location_update'),
    path('location/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='location_delete'),
]