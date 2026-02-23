from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='orders-list'),
    path('orders/<int:id>/', views.order_detail, name='orders-detail'),
    path('order-count/<int:business_user_id>/', views.order_count, name='order-count'),
    path('completed-order-count/<int:business_user_id>/', views.completed_order_count, name='completed-order-count'),
]
