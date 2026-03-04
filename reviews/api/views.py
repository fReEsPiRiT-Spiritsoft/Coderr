from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from reviews.models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from .permissions import IsCustomerUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsCustomerUser, IsReviewCreator


class ReviewListCreateAPIView(ListCreateAPIView):
    """
    GET  /api/reviews/ -> all reviews (auth required, can filter by business_user_id/reviewer_id)
    POST /api/reviews/ -> create review (only customer users, max 1 per business user)
    """
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

        # filters
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
    """
    GET    /api/reviews/{id}/ -> get review details
    PATCH  /api/reviews/{id}/ -> only reviewer can update (rating, description)
    DELETE /api/reviews/{id}/ -> only reviewer can delete (204 No Content)
    """
    queryset = Review.objects.select_related('business_user', 'reviewer').all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsReviewCreator]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return ReviewUpdateSerializer
        return ReviewSerializer

    def perform_destroy(self, instance):
        instance.delete()