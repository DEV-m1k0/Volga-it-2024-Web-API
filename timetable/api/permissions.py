


# SECTION - Права доступа для микросервиса Timetable



from rest_framework.permissions import BasePermission
from django.http.request import HttpRequest



class AdminOrManagerPermission(BasePermission):
    message = "Этот класс доступен только для администраторов и менеджеров."

    def has_object_permission(self, request: HttpRequest, view, obj):
        try:
            if request.user.is_superuser or request.user.roles.filter(role='Admin').exists() or request.user.roles.filter(role='Manager').exists():
                return True
            return False
        except:
            return False
    
    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)
    


class AdminOrManagerOrDoctorPermission(BasePermission):
    message = "Этот класс доступен только для администраторов, менеджеров и врачей."

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.roles.filter(role='Admin').exists() or request.user.roles.filter(role='Manager').exists() or request.user.roles.filter(role='Doctor').exists():
                return True
            return False
        except:
            return False
        
    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)
    


class AdminOrManagerOrPacientPermission(BasePermission):
    message = "Этот метод доступен только для администраторов, менеджеров и пациентов."

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.roles.filter(role='Admin').exists() or request.user.roles.filter(role='Manager').exists() or (request.user.roles.filter(role='User').exists() and request.user.appointments.all().exists()):
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)