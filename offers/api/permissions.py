"""Custom permissions for the offers API.

The module defines two permissions used by the offers views:
- `IsBusinessUser` restricts creation to users whose profile type is
  "business".
- `IsOfferOwner` permits read access to anyone but restricts write
  operations to the offer owner.
"""

from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """Allow only authenticated users with a business profile.

    The check is defensive: if a `Profile` is not attached to the
    `request.user` the permission is denied.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, "profile", None)
        return bool(profile and getattr(profile, "type", None) == "business")


class IsOfferOwner(permissions.BasePermission):
    """Allow only the offer owner to perform write operations.

    Safe (read-only) methods are allowed for any request. For
    non-safe methods we verify that the `request.user` is the owner of
    the provided offer instance.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and obj.user_id == request.user.id
        )