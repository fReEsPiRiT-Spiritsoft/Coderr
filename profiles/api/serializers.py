from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, required=False)
    email = serializers.EmailField(source='user.email', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at',
        )
        read_only_fields = ('user', 'username', 'email', 'created_at')

    def update(self, instance, validated_data):
        # Handle nested user data
        user_data = validated_data.pop('user', {})
        if 'first_name' in user_data:
            instance.user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            instance.user.last_name = user_data['last_name']
        instance.user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance