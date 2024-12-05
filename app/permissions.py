from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAdminUserWithMessage(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if not request.user.is_staff:
            raise PermissionDenied(detail="You must be an admin to access this informations.")
        return True

class IsAuthenticatedWithMessage(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="You must be authenticated to access this informations.")
        return True
