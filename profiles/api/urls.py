from django.urls import path
from .views import ProfileDetailAPIView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailAPIView.as_view(), name='api-profile-detail'),
]