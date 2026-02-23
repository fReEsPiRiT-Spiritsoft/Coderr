from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    - Safe methods (GET, HEAD, OPTIONS): any authenticated user allowed
    - Unsafe methods (PATCH/PUT/DELETE): only the owner of the profile allowed
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return obj.user == request.user