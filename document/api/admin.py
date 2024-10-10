from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Appointment)
admin.site.register(Role)
admin.site.register(Room)
admin.site.register(Hospital)
admin.site.register(MyUser)
admin.site.register(TimeTable)
admin.site.register(History)