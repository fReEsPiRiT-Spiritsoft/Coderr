from django.urls import path
from .views import CompletedOrderCountAPIView, OrderListCreateAPIView, OrderRetrieveUpdateAPIView, OrderCountAPIView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='api-orders-list'),
    path('orders/<int:id>/', OrderRetrieveUpdateAPIView.as_view(), name='api-order-detail'),
    path('order-count/<int:business_user_id>/', OrderCountAPIView.as_view(), name='api-order-count'),
     path('completed-order-count/<int:business_user_id>/', CompletedOrderCountAPIView.as_view(), name='api-completed-order-count'),
]