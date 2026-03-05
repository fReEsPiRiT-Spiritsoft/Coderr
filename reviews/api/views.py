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
        business_user_id = params.get('business_user_id')
        if business_user_id:
            try:
                qs = qs.filter(business_user_id=int(business_user_id))
            except ValueError:
                pass

        reviewer_id = params.get('reviewer_id')
        if reviewer_id:
            try:
                qs = qs.filter(reviewer_id=int(reviewer_id))
            except ValueError:
                pass

        ordering = params.get('ordering')
        allowed = {'updated_at', 'rating'}
        if ordering:
            key = ordering.lstrip('-')
            if key in allowed:
                qs = qs.order_by(ordering)
            else:
                qs = qs.order_by('-updated_at')
        else:
            qs = qs.order_by('-updated_at')

        return qs

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