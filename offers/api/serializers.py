from rest_framework import serializers
from django.contrib.auth.models import User
from offers.models import Offer, OfferDetail 


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ('id', 'url')


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)
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
        fields = ('url',)


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Offer
        fields = ('title', 'image', 'description', 'min_price', 'min_delivery_time', 'details')

    def validate_details(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("details must be a list")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        # create details
        objs = [OfferDetail(offer=offer, **d) for d in details_data]
        if objs:
            OfferDetail.objects.bulk_create(objs)
        return offer
    

class OfferDetailURLSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ('id', 'url')

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return f"/api/offerdetails/{obj.id}/"
        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")


class OfferRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id', read_only=True)
    image = serializers.ImageField(read_only=True, use_url=True)
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    details = OfferDetailURLSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = (
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'details')


# Write serializer for nested detail items on PATCH/POST
class OfferDetailUpdateSerializer(serializers.Serializer):
    # 'id' optional: if present, update existing detail; otherwise create new
    id = serializers.IntegerField(required=False)
    url = serializers.CharField(required=True, allow_blank=False)

    def validate(self, attrs):
        return attrs


class OfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailUpdateSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Offer
        fields = ('title', 'description', 'min_price', 'min_delivery_time', 'details')

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        # update simple fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # handle nested details: update existing or create new; do NOT delete unspecified details
        if details_data is not None:
            for d in details_data:
                detail_id = d.get('id')
                if detail_id:
                    try:
                        detail = OfferDetail.objects.get(pk=detail_id, offer=instance)
                    except OfferDetail.DoesNotExist:
                        raise serializers.ValidationError({'details': f'OfferDetail id={detail_id} not found for this offer.'})
                    # update allowed fields (here only url)
                    detail.url = d.get('url', detail.url)
                    detail.save()
                else:
                    # create new OfferDetail
                    OfferDetail.objects.create(offer=instance, url=d['url'])

        return instance
    

class OfferDetailRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    revisions = serializers.IntegerField()
    delivery_time_in_days = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    features = serializers.JSONField()  # expects list/JSON in model
    offer_type = serializers.CharField()

    class Meta:
        model = OfferDetail
        fields = (
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        )