from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OfferListSerializer, OfferCreateSerializer, OfferRetrieveSerializer, OfferUpdateSerializer, OfferDetailSerializer
from .permissions import IsBusinessUser, IsOfferOwner
from offers.models import Offer, OfferDetail
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class OfferPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

class OfferListCreateAPIView(ListCreateAPIView):
    """GET /api/offers/ and POST /api/offers/"""
    authentication_classes = [TokenAuthentication, SessionAuthentication]  
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        params = request.query_params
        min_price = params.get('min_price')
        if min_price is not None:
            try:
                float(min_price)
            except ValueError:
                return Response({'detail': 'Invalid value for min_price.'}, status=status.HTTP_400_BAD_REQUEST)
        max_delivery = params.get('max_delivery_time')
        if max_delivery is not None:
            try:
                int(max_delivery)
            except ValueError:
                return Response({'detail': 'Invalid value for max_delivery_time.'}, status=status.HTTP_400_BAD_REQUEST)
        creator_id = params.get('creator_id')
        if creator_id is not None:
            try:
                int(creator_id)
            except ValueError:
                return Response({'detail': 'Invalid value for creator_id.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Offer.objects.select_related('user').prefetch_related('details').all()
        params = self.request.query_params

        creator_id = params.get('creator_id')
        if creator_id:
            try:
                qs = qs.filter(user_id=int(creator_id))
            except ValueError:
                pass

        min_price = params.get('min_price')
        if min_price:
            try:
                qs = qs.filter(min_price__gte=float(min_price))
            except ValueError:
                pass

        max_delivery = params.get('max_delivery_time')
        if max_delivery:
            try:
                qs = qs.filter(min_delivery_time__lte=int(max_delivery))
            except ValueError:
                pass

        search = params.get('search')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))

        ordering = params.get('ordering')
        allowed = {'updated_at', 'min_price'}
        if ordering:
            key = ordering.lstrip('-')
            if key in allowed:
                qs = qs.order_by(ordering)
            else:
                qs = qs.order_by('-updated_at')
        else:
            qs = qs.order_by('-updated_at')

        return qs

class OfferRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/offers/{id}/"""
    queryset = Offer.objects.select_related('user').prefetch_related('details').all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOfferOwner]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    def perform_destroy(self, instance):
        instance.details.all().delete()
        instance.delete()


class OfferDetailRetrieveAPIView(RetrieveAPIView):
    """GET /api/offerdetails/{id}/"""
    queryset = OfferDetail.objects.select_related('offer').all()
    serializer_class = OfferDetailSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'