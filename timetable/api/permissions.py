from rest_framework.permissions import BasePermission
from django.http.request import HttpRequest

class AdminOrManagerPermission(BasePermission):
    message = "Этот класс доступен только для администраторов и менеджеров."

    def has_object_permission(self, request: HttpRequest, view, obj):
        if request.user.is_superuser or request.user.roles.filter(role='Admin').exists() or request.user.roles.filter(role='Manager').exists():
            return True
        return False
    
    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)