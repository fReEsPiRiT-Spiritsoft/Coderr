"""Serializers for the base information API.

The serializer here is a simple read-only representation used to
return aggregated platform statistics such as counts and average
ratings.
"""

from rest_framework import serializers


class BaseInfoSerializer(serializers.Serializer):
    """Representation for platform statistics.

    Fields provided:
    - ``review_count``: total number of reviews on the platform
    - ``average_rating``: average rating across all reviews
    - ``business_profile_count``: number of profiles with business role
    - ``offer_count``: total number of offers
    """

    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()