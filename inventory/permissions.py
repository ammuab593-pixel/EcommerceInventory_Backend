
from rest_framework.permissions import BasePermission, SAFE_METHODS


class VendorProductPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if not hasattr(user, 'profile'):
            return False

        role = user.profile.role

        # All registered roles can read products
        if request.method in SAFE_METHODS:
            return role in ['admin', 'vendor', 'end_user']

        # Only vendors can create, update and delete
        return role == 'vendor'

    def has_object_permission(self, request, view, obj):

        # All permitted roles can read products
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        # Vendors can modify only their own products
        return (
            user.profile.role == 'vendor'
            and obj.vendor_id == user.id
        )
