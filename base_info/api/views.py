"""API view that returns aggregated base/platform information.

The endpoint is intentionally permissive (AllowAny) since the data is
public. The view is defensive about the shape of the `Profile` model
and attempts several possible field names when counting business
profiles to remain compatible with different schema versions.
"""

from django.core.exceptions import FieldError
from django.db.models import Avg

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from offers.models import Offer
from profiles.models import Profile
from reviews.models import Review

from .serializers import BaseInfoSerializer


class BaseInfoAPIView(APIView):
    """Handle GET requests for platform statistics.

    The response contains counts for reviews, offers, business profiles
    and the average rating value (rounded to one decimal place).
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        """Return aggregated statistics as JSON."""

        try:
            review_count = Review.objects.count()
            avg_rating = Review.objects.aggregate(avg=Avg("rating"))["avg"] or 0.0
            try:
                business_profile_count = Profile.objects.filter(type="business").count()
            except FieldError:
                try:
                    business_profile_count = Profile.objects.filter(role="business").count()
                except FieldError:
                    try:
                        business_profile_count = Profile.objects.filter(is_business=True).count()
                    except FieldError:
                        business_profile_count = 0
            offer_count = Offer.objects.count()
            data = {
                "review_count": review_count,
                "average_rating": round(float(avg_rating), 1),
                "business_profile_count": business_profile_count,
                "offer_count": offer_count,
            }
            serializer = BaseInfoSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": "Internal server error retrieving base info."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )