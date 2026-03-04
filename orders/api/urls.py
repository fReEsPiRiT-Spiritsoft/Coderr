"""URL routes for the orders API.

Defines endpoints for listing/creating orders, retrieving/updating a
single order and counting orders for a business user.
"""

from django.urls import path

from .views import (
    CompletedOrderCountAPIView,
    OrderCountAPIView,
    OrderListCreateAPIView,
    OrderRetrieveUpdateAPIView,
)

urlpatterns = [
    path("orders/", OrderListCreateAPIView.as_view(), name="api-orders-list"),
    path("orders/<int:id>/", OrderRetrieveUpdateAPIView.as_view(), name="api-order-detail"),
    path("order-count/<int:business_user_id>/", OrderCountAPIView.as_view(), name="api-order-count"),
    path(
        "completed-order-count/<int:business_user_id>/",
        CompletedOrderCountAPIView.as_view(),
        name="api-completed-order-count",
    ),
]