from django.urls import path
from . import views

urlpatterns = [
    path('inventory/list/', views.InventoryListView.as_view(), name='inventory_list'),
    path('inventory/<int:pk>/detail/', views.InventoryDetailView.as_view(), name='inventory_detail'),
    path('inventory/<int:pk>/update/', views.InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.InventoryDeleteView.as_view(), name='inventory_delete'),
    
    path('inventory/<str:site>/<str:subsite>/', views.InventoryListView.as_view(), name='inventory_list_argument'),
]