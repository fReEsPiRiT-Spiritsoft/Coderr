"""Serializers for the reviews API.

Includes serializers for reading, creating and updating reviews. The
create serializer enforces one review per reviewer/business pair.
"""

from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reading `Review` instances."""

    business_user = serializers.IntegerField(source='business_user.id', read_only=True)
    reviewer = serializers.IntegerField(source='reviewer.id', read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = Review
        fields = (
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'business_user', 'reviewer', 'created_at', 'updated_at')

class ReviewCreateSerializer(serializers.Serializer):
    """Create a new review.

    Validates that the target business user exists and that the reviewer
    has not already left a review for the same business user.
    """

    business_user = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_business_user(self, value):
        from django.contrib.auth.models import User
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Business user not found.")
        return value

    def validate(self, data):
        from django.contrib.auth.models import User
        reviewer = self.context['request'].user
        business_user_id = data['business_user']
        if Review.objects.filter(reviewer=reviewer, business_user_id=business_user_id).exists():
            raise serializers.ValidationError("You can only leave one review per business user.")
        return data

    def create(self, validated_data):
        reviewer = self.context['request'].user
        review = Review.objects.create(
            reviewer=reviewer,
            business_user_id=validated_data['business_user'],
            rating=validated_data['rating'],
            description=validated_data.get('description', '')
        )
        return review
    

class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer used to update rating and description of a review."""

    class Meta:
        model = Review
        fields = ("rating", "description")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value