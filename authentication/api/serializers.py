from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    type = serializers.ChoiceField(choices=('customer', 'business'), default='customer')
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already exists.")]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already exists.")]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeated_password', 'type')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('repeated_password'):
            raise serializers.ValidationError({'repeated_password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('repeated_password', None)
        user_type = validated_data.pop('type', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        # optional: persist user_type to related profile here
        return user
    
class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    def validate(self, attrs):
        self.username = attrs.get('username')
        self.password = attrs.get('password')
        if not self.username or not self.password:
            raise serializers.ValidationError('username and password are required.')
        user = authenticate(username=self.username, password=self.password)
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        attrs['user'] = user
        return attrs
