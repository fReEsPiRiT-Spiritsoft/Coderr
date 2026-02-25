from django.urls import path
from .views import OfferListCreateAPIView, OfferRetrieveUpdateAPIView, OfferDetailRetrieveAPIView

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='api-offers-list'),
    path('offers/<int:id>/', OfferRetrieveUpdateAPIView.as_view(), name='api-offer-detail'),
    path('offerdetails/<int:id>/', OfferDetailRetrieveAPIView.as_view(), name='api-offerdetail'),
]