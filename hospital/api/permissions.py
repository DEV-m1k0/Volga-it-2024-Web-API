


# SECTION - Права доступа для микросервиса Hospital



from rest_framework.permissions import BasePermission, IsAuthenticated
from api.models import MyUser


class IsAdminUser(BasePermission):
    message = "Этот класс доступен только для администраторов."

    def has_permission(self, request, view):
        try:
            user: MyUser = request.user
            has_role = user.roles.all().filter(role="Admin").exists()
            return has_role
        except:
            return False