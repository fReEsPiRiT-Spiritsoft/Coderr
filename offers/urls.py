from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.offer_list, name='offers-list'),
    path('offers/<int:id>/', views.offer_detail, name='offers-detail'),
    path('offerdetails/<int:id>/', views.offer_details, name='offers-details-extended'),
]
