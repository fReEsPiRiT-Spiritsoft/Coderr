from rest_framework import permissions

class IsBusinessUser(permissions.BasePermission):
    """
    Allow only authenticated users whose profile.type == 'business'.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, 'profile', None)
        return bool(profile and getattr(profile, 'type', None) == 'business')
    

class IsOfferOwner(permissions.BasePermission):
    """
    Only the offer owner can modify (PATCH/PUT/DELETE). Authenticated users can read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and obj.user_id == request.user.id