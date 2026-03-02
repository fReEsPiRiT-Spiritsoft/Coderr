from django.urls import path
from .views import OrderListCreateAPIView, OrderRetrieveUpdateAPIView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='api-orders-list'),
    path('orders/<int:id>/', OrderRetrieveUpdateAPIView.as_view(), name='api-order-detail'),
]