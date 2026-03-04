from rest_framework import serializers
from django.contrib.auth.models import User
from offers.models import Offer, OfferDetail 


class OfferDetailSerializer(serializers.ModelSerializer):
    """Retrieve single OfferDetail - GET /api/offerdetails/{id}/"""
    class Meta:
        model = OfferDetail
        fields = ('id', 'title', 'price', 'delivery_time_in_days', 'revisions', 'features', 'offer_type')


class OfferDetailListSerializer(serializers.ModelSerializer):
    """For listing offers with nested details"""
    class Meta:
        model = OfferDetail
        fields = ('id', 'title', 'price', 'delivery_time_in_days', 'revisions', 'offer_type')


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailListSerializer(many=True, read_only=True)
    user_details = UserSummarySerializer(source='user', read_only=True)
    image = serializers.ImageField(read_only=True, use_url=True)
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = Offer
        fields = (
            'id', 'user', 'user_details', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time'
        )
        read_only_fields = ('id', 'user', 'user_details', 'created_at', 'updated_at', 'details')


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ('title', 'price', 'delivery_time_in_days', 'revisions', 'features', 'offer_type')


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Offer
        fields = ('title', 'image', 'description', 'min_price', 'min_delivery_time', 'details')

    def create(self, validated_data):
        # user kommt von serializer.save(user=...) in validated_data
        user = validated_data.pop('user')
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(user=user, **validated_data)
        objs = [OfferDetail(offer=offer, **d) for d in details_data]
        if objs:
            OfferDetail.objects.bulk_create(objs)
        return offer


class OfferRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id', read_only=True)
    image = serializers.ImageField(read_only=True, use_url=True)
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    details = OfferDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = (
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'details')


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ('id', 'title', 'price', 'delivery_time_in_days', 'revisions', 'features', 'offer_type')


class OfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailUpdateSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Offer
        fields = ('title', 'description', 'image', 'min_price', 'min_delivery_time', 'details')

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            for d in details_data:
                detail_id = d.get('id')
                if detail_id:
                    try:
                        detail = OfferDetail.objects.get(pk=detail_id, offer=instance)
                        for attr, value in d.items():
                            if attr != 'id':
                                setattr(detail, attr, value)
                        detail.save()
                    except OfferDetail.DoesNotExist:
                        raise serializers.ValidationError({'details': f'OfferDetail id={detail_id} not found.'})
                else:
                    OfferDetail.objects.create(offer=instance, **{k: v for k, v in d.items() if k != 'id'})

        return instance