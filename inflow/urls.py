from django.urls import path
from . import views

urlpatterns = [
    path('inflow/list/', views.InflowListView.as_view(), name='inflow_list'),
    path('inflow/create/', views.InflowCreateView.as_view(), name='inflow_create'),
    path('inflow/<int:pk>/details/', views.InflowDetailView.as_view(), name='inflow_detail'),
    path('inflow/<int:pk>/add/', views.InflowAddView.as_view(), name='inflow_add')
]