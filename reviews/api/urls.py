from django.urls import path
from .views import ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('reviews/', ReviewListCreateAPIView.as_view(), name='api-reviews-list'),
    path('reviews/<int:id>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='api-review-detail'),
]