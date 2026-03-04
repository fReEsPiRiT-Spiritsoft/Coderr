"""Permissions used by the reviews API.

Provides permission checks ensuring only customer users can create
reviews and only the original reviewer can modify or delete their
review.
"""

from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Allow access only to authenticated users with a customer profile."""

    def has_permission(self, request, view):
        user = request.user
        profile = getattr(user, "profile", None)
        return bool(user and user.is_authenticated and profile and getattr(profile, "type", None) == "customer")


class IsReviewCreator(permissions.BasePermission):
    """Allow object-level updates only for the original reviewer."""

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj.reviewer_id == request.user.id