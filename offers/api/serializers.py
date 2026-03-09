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

    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    delivery_time_in_days = serializers.IntegerField(min_value=1)
    revisions = serializers.IntegerField(min_value=-1)
    offer_type = serializers.ChoiceField(choices=["basic", "standard", "premium"])

    class Meta:
        model = OfferDetail
        fields = ("title", "price", "delivery_time_in_days", "revisions", "features", "offer_type")


class OfferCreateSerializer(serializers.ModelSerializer):
    """Create serializer for `Offer` including optional nested details."""

    details = OfferDetailCreateSerializer(many=True, write_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    min_delivery_time = serializers.IntegerField(min_value=1, required=False)

    class Meta:
        model = Offer
        fields = ("title", "image", "description", "min_price", "min_delivery_time", "details")

    def validate_details(self, value):
        """Ensure exactly 3 details with unique offer_types basic/standard/premium."""
        if len(value) != 3:
            raise serializers.ValidationError("An offer must contain exactly 3 details.")
        offer_types = sorted([d.get("offer_type") for d in value])
        if offer_types != ["basic", "premium", "standard"]:
            raise serializers.ValidationError(
                "Details must contain exactly one each of: basic, standard, premium."
            )
        return value

    def create(self, validated_data):
        """Create `Offer` and associated `OfferDetail` instances."""
        user = validated_data.pop("user")
        details_data = validated_data.pop("details", [])
        offer = Offer.objects.create(user=user, **validated_data)
        objs = [OfferDetail(offer=offer, **d) for d in details_data]
        if objs:
            OfferDetail.objects.bulk_create(objs)
            details = offer.details.all()
            offer.min_price = min(d.price for d in details)
            offer.min_delivery_time = min(d.delivery_time_in_days for d in details)
            offer.save(update_fields=["min_price", "min_delivery_time"])
        return offer

    def to_representation(self, instance):
        """Return full offer data including id and details after creation."""
        return OfferRetrieveSerializer(instance, context=self.context).data



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

    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    delivery_time_in_days = serializers.IntegerField(min_value=1, required=False)
    revisions = serializers.IntegerField(min_value=-1, required=False)
    offer_type = serializers.ChoiceField(choices=["basic", "standard", "premium"], required=False)

    class Meta:
        model = OfferDetail
        fields = ("id", "title", "price", "delivery_time_in_days", "revisions", "features", "offer_type")


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Update serializer for `Offer` supporting nested detail updates."""

    details = OfferDetailUpdateSerializer(many=True, required=False, write_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    min_delivery_time = serializers.IntegerField(min_value=1, required=False)

    class Meta:
        model = Offer
        fields = ("title", "description", "image", "min_price", "min_delivery_time", "details")

    def validate_details(self, value):
        """Ensure each detail has either id or offer_type for matching."""
        for d in value:
            if not d.get("id") and not d.get("offer_type"):
                raise serializers.ValidationError(
                    "Each detail must have either 'id' or 'offer_type' to identify which detail to update."
                )
        return value

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
                    offer_type = d.get("offer_type")
                    if offer_type:
                        existing = OfferDetail.objects.filter(offer=instance, offer_type=offer_type).first()
                        if existing:
                            for attr, value in d.items():
                                setattr(existing, attr, value)
                            existing.save()
                        else:
                            OfferDetail.objects.create(offer=instance, **d)
                    else:
                        OfferDetail.objects.create(offer=instance, **d)

            details = instance.details.all()
            if details.exists():
                instance.min_price = min(d.price for d in details)
                instance.min_delivery_time = min(d.delivery_time_in_days for d in details)
                instance.save(update_fields=["min_price", "min_delivery_time"])

        return instance

    def to_representation(self, instance):
        """Return full offer data including id and details after update."""
        return OfferRetrieveSerializer(instance, context=self.context).data