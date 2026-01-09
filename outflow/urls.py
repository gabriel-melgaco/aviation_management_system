from django.urls import path
from . import views

urlpatterns = [
    path('outflow/list/', views.OutflowListView.as_view(), name='outflow_list'),
    path('outflow/<int:pk>/details/', views.OutflowDetailView.as_view(), name='outflow_detail'),
    path('outflow/<int:pk>/move/', views.OutflowMoveView.as_view(), name='outflow_move')
]