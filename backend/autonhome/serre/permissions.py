from rest_framework import permissions

class IsUserOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET requests for all
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner or if admin.
        return obj == request.user or request.user.is_staff
