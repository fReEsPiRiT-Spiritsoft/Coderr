from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list, name='reviews-list'),
    path('reviews/<int:id>/', views.review_detail, name='reviews-detail'),
]
