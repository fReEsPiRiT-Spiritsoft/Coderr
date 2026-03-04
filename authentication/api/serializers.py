"""Serializers for authentication API.

This module contains the registration and login serializers used by the
authentication endpoints. The serializers perform validation and create
or authenticate Django `User` objects. When a user is created we also
ensure a related `Profile` object exists and its `type` is set.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from profiles.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate and create new user registrations.

    Fields:
    - `username`, `email`, `password`, `repeated_password`, `type`

    The serializer enforces unique username/email and that the provided
    passwords match. On creation it also creates or updates the related
    `Profile` with the requested `type` (defaults to 'customer').
    """

    repeated_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    type = serializers.ChoiceField(choices=("customer", "business"), default="customer")
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="Email already exists."
            )
        ]
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="Username already exists."
            )
        ]
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "repeated_password",
            "type",
        )

    def validate(self, attrs):
        """Ensure password and repeated_password match."""
        if attrs.get("password") != attrs.get("repeated_password"):
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """Create the user and associated profile.

        `repeated_password` is removed, and `type` is used to set the
        `Profile.type`. The `password` value is passed to
        `User.objects.create_user` which handles hashing.
        """

        validated_data.pop("repeated_password", None)
        user_type = validated_data.pop("type", "customer")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)

        if hasattr(user, "profile"):
            user.profile.type = user_type
            user.profile.save()
        else:
            Profile.objects.create(user=user, type=user_type)

        return user


class LoginSerializer(serializers.Serializer):
    """Authenticate a user with username and password.

    On successful validation the authenticated `user` instance is
    attached under the `user` key in `validated_data`.
    """

    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    def validate(self, attrs):
        """Validate credentials and authenticate the user."""

        self.username = attrs.get("username")
        self.password = attrs.get("password")
        if not self.username or not self.password:
            raise serializers.ValidationError("username and password are required.")

        user = authenticate(username=self.username, password=self.password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        attrs["user"] = user
        return attrs