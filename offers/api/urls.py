from django.urls import path
from .views import OfferListCreateAPIView, OfferRetrieveUpdateDestroyAPIView, OfferDetailRetrieveAPIView

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='api-offers-list'),
    path('offers/<int:id>/', OfferRetrieveUpdateDestroyAPIView.as_view(), name='api-offer-detail'),
    path('offerdetails/<int:id>/', OfferDetailRetrieveAPIView.as_view(), name='api-offerdetail-detail'),
]