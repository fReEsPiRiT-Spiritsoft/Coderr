"""Serializers for the offers API.

The module provides separate serializers for list, retrieve and create
operations. Nested `OfferDetail` objects are represented with their
own serializers and the create/update paths support writing nested
details.
"""

from django.contrib.auth.models import User

from rest_framework import serializers

from offers.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializer for a single `OfferDetail` used on detail endpoints."""

    class Meta:
        model = OfferDetail
        fields = (
            "id",
            "title",
            "price",
            "delivery_time_in_days",
            "revisions",
            "features",
            "offer_type",
        )


class OfferDetailListSerializer(serializers.ModelSerializer):
    """Compact serializer used when listing nested details."""

    class Meta:
        model = OfferDetail
        fields = (
            "id",
            "title",
            "price",
            "delivery_time_in_days",
            "revisions",
            "offer_type",
        )


class UserSummarySerializer(serializers.ModelSerializer):
    """A small user summary used on offers list responses."""

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class OfferListSerializer(serializers.ModelSerializer):
    """Serializer for listing `Offer` instances with nested details."""

    details = OfferDetailListSerializer(many=True, read_only=True)
    user_details = UserSummarySerializer(source="user", read_only=True)
    image = serializers.ImageField(read_only=True, use_url=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Offer
        fields = (
            "id",
            "user",
            "user_details",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        )
        read_only_fields = ("id", "user", "user_details", "created_at", "updated_at", "details")


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """Serializer used to create nested `OfferDetail` objects."""

    class Meta:
        model = OfferDetail
        fields = ("title", "price", "delivery_time_in_days", "revisions", "features", "offer_type")


class OfferCreateSerializer(serializers.ModelSerializer):
    """Create serializer for `Offer` including optional nested details."""

    details = OfferDetailCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Offer
        fields = ("title", "image", "description", "min_price", "min_delivery_time", "details")

    def create(self, validated_data):
        """Create `Offer` and associated `OfferDetail` instances.

        The `user` is expected to be provided by the view via
        `serializer.save(user=request.user)`.
        """

        user = validated_data.pop("user")
        details_data = validated_data.pop("details", [])
        offer = Offer.objects.create(user=user, **validated_data)
        objs = [OfferDetail(offer=offer, **d) for d in details_data]
        if objs:
            OfferDetail.objects.bulk_create(objs)
        return offer


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a single `Offer` with full details."""

    user = serializers.IntegerField(source="user.id", read_only=True)
    image = serializers.ImageField(read_only=True, use_url=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    details = OfferDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = (
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at", "details")


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    """Serializer used to update existing `OfferDetail` objects."""

    class Meta:
        model = OfferDetail
        fields = ("id", "title", "price", "delivery_time_in_days", "revisions", "features", "offer_type")


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Update serializer for `Offer` supporting nested detail updates."""

    details = OfferDetailUpdateSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Offer
        fields = ("title", "description", "image", "min_price", "min_delivery_time", "details")

    def update(self, instance, validated_data):
        """Update the offer and apply changes to nested details.

        If `details` is provided the serializer will either update
        existing `OfferDetail` objects (when an `id` is present) or
        create new ones otherwise.
        """

        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            for d in details_data:
                detail_id = d.get("id")
                if detail_id:
                    try:
                        detail = OfferDetail.objects.get(pk=detail_id, offer=instance)
                        for attr, value in d.items():
                            if attr != "id":
                                setattr(detail, attr, value)
                        detail.save()
                    except OfferDetail.DoesNotExist:
                        raise serializers.ValidationError({"details": f"OfferDetail id={detail_id} not found."})
                else:
                    OfferDetail.objects.create(offer=instance, **{k: v for k, v in d.items() if k != "id"})

        return instance