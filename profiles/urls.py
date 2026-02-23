from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>/', views.profile_detail, name='profile-detail'),
    path('profiles/business/', views.business_profiles, name='profiles-business'),
    path('profiles/customer/', views.customer_profiles, name='profiles-customer'),
]
