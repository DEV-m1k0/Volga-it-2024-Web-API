from rest_framework.permissions import BasePermission

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
    

class DoctorOrPacientPermission(BasePermission):
    message = "Этот класс доступен только для врачей и пациентов."

    def has_object_permission(self, request, view, obj):
        if request.user.roles.filter(role='Doctor').exists():
            return True
        elif request.user.roles.filter(role='User').exists() and request.user.appointments.all().exists():
            return True
        

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)