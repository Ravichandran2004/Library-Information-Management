from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user.is_staff  # Only admin can modify


# from rest_framework.permissions import BasePermission, SAFE_METHODS
#
# class IsAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
#             return True
#         return request.user.is_staff  # Only admin can modify
