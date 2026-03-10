"""Views for the reviews API.

List and detail endpoints for reviews. Creation is restricted to
customer users while retrieve/update/delete operations are performed
by the original reviewer.
"""

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reviews.models import Review

from .permissions import IsCustomerUser, IsReviewCreator
from .serializers import ReviewCreateSerializer, ReviewSerializer, ReviewUpdateSerializer
from .filters import validate_list_params, apply_review_filters


class ReviewListCreateAPIView(ListCreateAPIView):
    """GET /api/reviews/ and POST /api/reviews/."""

    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        qs = Review.objects.select_related('business_user', 'reviewer').all()
        params = self.request.query_params
        # Delegiere Filter-Anwendung an helpers in reviews.api.filters
        return apply_review_filters(qs, params)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        output_serializer = ReviewSerializer(review)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single review.
    Only the original reviewer may update or delete their review.
    """
    queryset = Review.objects.select_related("business_user", "reviewer").all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsReviewCreator]
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return ReviewUpdateSerializer
        return ReviewSerializer

    def update(self, request, *args, **kwargs):
        """Update review and return full representation via ReviewSerializer."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = ReviewUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()