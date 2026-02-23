from django.urls import path
from . import views

urlpatterns = [
    path('base-info/', views.base_info, name='base-info'),
]
