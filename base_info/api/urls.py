"""URL configuration for the base information API.

Provides a single endpoint that returns aggregated platform metrics.
"""

from django.urls import path

from .views import BaseInfoAPIView

urlpatterns = [
    path("base-info/", BaseInfoAPIView.as_view(), name="api-base-info"),
]