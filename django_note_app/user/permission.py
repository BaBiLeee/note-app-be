from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsAdminUser(BasePermission):
    """
    Chỉ cho phép người dùng có quyền admin truy cập API này.
    """
    def has_permission(self, request, view):
        # Kiểm tra xem token có hợp lệ và người dùng có quyền admin không
        if request.user and request.user.is_authenticated and request.user.admin:
            return True
        return False
