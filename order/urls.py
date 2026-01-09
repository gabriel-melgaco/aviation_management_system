from django.urls import path
from . import views


urlpatterns = [
    # URLS Order
    path('order/list/', views.OrderListView.as_view(), name='order_list'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/details/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),

    # URLS Order Item
    path('order/item/list/', views.OrderItemListView.as_view(), name='order_item_list'),
    path('order/<int:pk>/item/create/', views.OrderItemCreateView.as_view(), name='order_item_create'),
    path('order/item/<int:pk>/update/', views.OrderItemUpdateView.as_view(), name='order_item_update'),
    path('order/item/<int:pk>/delete/', views.OrderItemDeleteView.as_view(), name='order_item_delete'),

    # Export archive
    path('order/<int:pk>/export_archive/', views.OrderExportArchive.as_view(), name='order_export_archive'),
]