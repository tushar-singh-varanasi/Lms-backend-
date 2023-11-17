# permissions.py

from rest_framework.permissions import BasePermission

class IsLibrarianOrReadOnly(BasePermission):
    """
    Custom permission to only allow librarians to perform CRUD operations.
    """
    def has_permission(self, request, view):
        # Allow read permissions to any user (authenticated or not).
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Check if the user is in the 'Librarian' group.
        return 'Librarian' in [group.name for group in request.user.groups.all()]
