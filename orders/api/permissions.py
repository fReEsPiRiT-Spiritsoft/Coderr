from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    """Only authenticated users with profile.type == 'customer'"""
    def has_permission(self, request, view):
        user = request.user
        profile = getattr(user, 'profile', None)
        return bool(user and user.is_authenticated and profile and getattr(profile, 'type', None) == 'customer')


class IsBusinessUserOfOrder(permissions.BasePermission):
    """Only the business_user of an order can update it"""
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj.business_user_id == request.user.id
    

class IsAdminUser(permissions.BasePermission):
    """Only admin/staff users can delete orders"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)