"""Permissions used by the profiles API.

Currently defines a single permission that allows read access for any
authenticated user and restricts update/delete operations to the
profile owner.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow safe methods for authenticated users, unsafe for owner only.

    Safe methods (GET, HEAD, OPTIONS) are permitted for any authenticated
    user. Unsafe methods (PATCH/PUT/DELETE) are only allowed if the
    requesting user owns the `Profile` instance.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return obj.user == request.user