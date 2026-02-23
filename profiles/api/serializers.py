from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Profile
from rest_framework.validators import UniqueValidator

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    email = serializers.EmailField(source='user.email', required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    file = serializers.ImageField(required=False, allow_null=True, use_url=True)
    location = serializers.CharField(required=False, allow_blank=True)
    tel = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    working_hours = serializers.CharField(required=False, allow_blank=True)
    type = serializers.ChoiceField(choices=Profile.TYPE_CHOICES, required=False)

    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = Profile
        fields = (
            'user', 'username', 'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours',
            'type', 'email', 'created_at'
        )

    def validate(self, attrs):
        string_fields = ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours')
        for f in string_fields:
            if attrs.get(f) is None:
                attrs[f] = ''
        return attrs

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', {}) 
        email = user_data.get('email') if user_data else None
        if email is not None and email != instance.user.email:
            if User.objects.exclude(pk=instance.user.pk).filter(email=email).exists():
                raise serializers.ValidationError({'email': 'Email already exists.'})
            instance.user.email = email
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance