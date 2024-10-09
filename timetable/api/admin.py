from django.contrib import admin
from .models import TimeTable, MyUser, Role, Room, Hospital, Apointment

# Register your models here.


admin.site.register(TimeTable)
admin.site.register(MyUser)
admin.site.register(Role)
admin.site.register(Room)
admin.site.register(Hospital)
admin.site.register(Apointment)