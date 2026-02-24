from django.urls import path
from .views import CustomerProfilesAPIView, BusinessProfilesAPIView, ProfileDetailAPIView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailAPIView.as_view(), name='api-profile-detail'),
    path('profiles/business/', BusinessProfilesAPIView.as_view(), name='api-profiles-business'),
    path('profiles/customer/', CustomerProfilesAPIView.as_view(), name='api-profiles-customer'),
]