"""URL routes for the offers API.

Provides listing/creation of offers as well as retrieve/update/delete
endpoints for individual offers and offer details.
"""

from django.urls import path

from .views import (
    OfferDetailRetrieveAPIView,
    OfferListCreateAPIView,
    OfferRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("offers/", OfferListCreateAPIView.as_view(), name="api-offers-list"),
    path("offers/<int:id>/", OfferRetrieveUpdateDestroyAPIView.as_view(), name="api-offer-detail"),
    path("offerdetails/<int:id>/", OfferDetailRetrieveAPIView.as_view(), name="api-offerdetail-detail"),
]

