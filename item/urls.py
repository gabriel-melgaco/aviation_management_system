from django.urls import path
from . import views

urlpatterns = [
    path('item/list/', views.ItemListView.as_view(), name='item_list'),
    path('item/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('item/<int:pk>/details/', views.ItemDetailView.as_view(), name='item_detail'),
    path('item/<int:pk>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    #Item Equivalent urls:
    path('item/equivalent/list/', views.ItemEquivalentListView.as_view(), name='item_list_equivalent'),
    path('item/equivalent/create/', views.ItemEquivalentCreateView.as_view(), name='item_create_equivalent'),
    path('item/<int:pk>/equivalent/delete/', views.ItemEquivalentDeleteView.as_view(), name='item_delete_equivalent'),

]