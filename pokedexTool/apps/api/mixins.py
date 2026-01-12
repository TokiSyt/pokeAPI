from typing import Any

from rest_framework import permissions


class AdminUserPermissionMixin:
    permission_classes: Any = [permissions.IsAdminUser]
