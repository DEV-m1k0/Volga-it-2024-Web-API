from django.contrib import admin
from .models import MyUser, Role

# Register your models here.

admin.site.register(MyUser)
admin.site.register(Role)