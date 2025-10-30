from rest_framework import permissions

class AdminUserPermissionMixin():
    permission_classes = [permissions.IsAdminUser]