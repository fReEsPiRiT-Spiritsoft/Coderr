"""URL routes for the reviews API.

Provides endpoints to list/create reviews and to retrieve/update/delete
individual reviews.
"""

from django.urls import path

from .views import ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("reviews/", ReviewListCreateAPIView.as_view(), name="api-reviews-list"),
    path("reviews/<int:id>/", ReviewRetrieveUpdateDestroyAPIView.as_view(), name="api-review-detail"),
]