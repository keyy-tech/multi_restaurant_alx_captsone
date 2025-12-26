from rest_framework.permissions import BasePermission


class IsOwnerUser(BasePermission):
    message = "Only owners can create restaurants"

    def has_permission(self, request, view):
        # Must be authenticated and role must be 'owner'
        return request.user.is_authenticated and request.user.role == "owner"
