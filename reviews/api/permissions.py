from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Only authenticated users with profile.type == 'customer'"""
    def has_permission(self, request, view):
        user = request.user
        profile = getattr(user, 'profile', None)
        return bool(user and user.is_authenticated and profile and getattr(profile, 'type', None) == 'customer')
    
class IsReviewCreator(permissions.BasePermission):
    """Only the reviewer who created the review can update it"""
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj.reviewer_id == request.user.id