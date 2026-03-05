"""Serializers for profile API.

The `ProfileSerializer` exposes profile fields along with a small
subset of related user fields. The serializer handles updates to the
linked `User` first/last name when provided.
"""

from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize and update `Profile` instances.

    Read-only user information (id, username, email) is included. The
    `update` method ensures that nested user attributes such as
    `first_name`/`last_name` are saved on the related `User` object.
    """

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", allow_blank=True, required=False)
    last_name = serializers.CharField(source="user.last_name", allow_blank=True, required=False)
    email = serializers.EmailField(source="user.email", required=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        )
        read_only_fields = ("user", "username", "created_at")

    def update(self, instance, validated_data):
        """Apply updates to the profile and nested user fields.

        If `first_name` or `last_name` are provided under the `user`
        key they are set on the related `User` before saving the
        `Profile` instance.
        """

        user_data = validated_data.pop("user", {})
        if "first_name" in user_data:
            instance.user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            instance.user.last_name = user_data["last_name"]
        if "email" in user_data:
            instance.user.email = user_data["email"]
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance