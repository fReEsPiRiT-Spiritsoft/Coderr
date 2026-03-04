from django.urls import path
from .views import BaseInfoAPIView

urlpatterns = [
    path('base-info/', BaseInfoAPIView.as_view(), name='api-base-info'),
]