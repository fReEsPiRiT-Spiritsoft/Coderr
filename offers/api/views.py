
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .serializers import OfferListSerializer, OfferCreateSerializer, OfferRetrieveSerializer, OfferUpdateSerializer
from .permissions import IsBusinessUser
from offers.models import Offer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.generics import RetrieveAPIView
from .serializers import OfferRetrieveSerializer, OfferDetailRetrieveSerializer
from .permissions import IsOfferOwner
from offers.models import OfferDetail
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class OfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferListCreateAPIView(ListCreateAPIView):
    """
    GET  /api/offers/    -> public list (supports filters/search/ordering/pagination)
    POST /api/offers/    -> create offer, only for authenticated users with business profile
    """
    authentication_classes = [TokenAuthentication] 
    pagination_class = OfferPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

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



class OfferRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    GET  /api/offers/{id}/   -> authenticated users can read
    PATCH /api/offers/{id}/  -> only creator (owner) can modify; partial update supported
    """
    queryset = Offer.objects.select_related('user').prefetch_related('details').all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOfferOwner]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    def perform_update(self, serializer):
        # ensure owner cannot change the 'user' field implicitly via nested data
        serializer.save()

class OfferRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET  /api/offers/{id}/   -> authenticated users can read
    PATCH /api/offers/{id}/  -> only creator (owner) can modify; partial update supported
    DELETE /api/offers/{id}/ -> only creator (owner) can delete (204 No Content)
    """
    queryset = Offer.objects.select_related('user').prefetch_related('details').all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOfferOwner]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    def perform_update(self, serializer):
        serializer.save()

    # optional: explicit perform_destroy to ensure any cleanup
    def perform_destroy(self, instance):
        # delete related details first (if any custom cleanup needed)
        instance.details.all().delete()
        instance.delete()



class OfferDetailRetrieveAPIView(RetrieveAPIView):
    """
    GET /api/offerdetails/{id}/
    - Auth required (TokenAuthentication)
    - 200: offer detail object
    - 401: unauthenticated
    - 404: not found
    """
    queryset = OfferDetail.objects.select_related('offer').all()
    serializer_class = OfferDetailRetrieveSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'