from rest_framework import serializers
from orders.models import Order 
from offers.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.IntegerField(source='customer_user.id', read_only=True)
    business_user = serializers.IntegerField(source='business_user.id', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    features = serializers.JSONField()
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = Order
        fields = (
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'customer_user', 'business_user', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        try:
            detail = OfferDetail.objects.select_related('offer', 'offer__user').get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("OfferDetail not found.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        offer_detail = OfferDetail.objects.select_related('offer', 'offer__user').get(pk=validated_data['offer_detail_id'])
        offer = offer_detail.offer
        business_user = offer.user
        order = Order.objects.create(
            customer_user=user,
            business_user=business_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'
        )
        return order
    
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return value