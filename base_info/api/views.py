from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Avg
from django.core.exceptions import FieldError

from offers.models import Offer
from reviews.models import Review
from profiles.models import Profile
from .serializers import BaseInfoSerializer


class BaseInfoAPIView(APIView):
    """GET /api/base-info/ - Plattform-Statistiken"""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        try:
            review_count = Review.objects.count()
            avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0.0
            # try common profile fields to count business profiles
            try:
                business_profile_count = Profile.objects.filter(type='business').count()
            except FieldError:
                try:
                    business_profile_count = Profile.objects.filter(role='business').count()
                except FieldError:
                    try:
                        business_profile_count = Profile.objects.filter(is_business=True).count()
                    except FieldError:
                        business_profile_count = 0

            offer_count = Offer.objects.count()

            data = {
                'review_count': review_count,
                'average_rating': round(float(avg_rating), 1),
                'business_profile_count': business_profile_count,
                'offer_count': offer_count
            }
            serializer = BaseInfoSerializer(data)
            return Response(serializer.data, status=200)
        except Exception as exc:
            return Response({'detail': 'Internal server error retrieving base info.'}, status=500)