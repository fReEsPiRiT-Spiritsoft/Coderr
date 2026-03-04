"""Permissions for orders API.

This module contains small permission classes used by the orders
endpoints to ensure only the appropriate users can create, update or
delete orders.
"""

from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Allow access only to authenticated customer users."""

    def has_permission(self, request, view):
        user = request.user
        profile = getattr(user, "profile", None)
        return bool(user and user.is_authenticated and profile and getattr(profile, "type", None) == "customer")


class IsBusinessUserOfOrder(permissions.BasePermission):
    """Allow object-level access only to the business side of an order."""

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj.business_user_id == request.user.id


class IsAdminUser(permissions.BasePermission):
    """Allow access only to staff/admin users for destructive actions."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)