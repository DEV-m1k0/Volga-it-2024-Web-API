from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.



# Список ролей
CHOICES_ROLE_FOR_MYUSER = [
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('doctor', 'Doctor'),
    ('user', 'User')
]


ROLES = ['Admin', 'Manager', 'Doctor', 'User']


class Role(models.Model):
    role = models.CharField(max_length=20)

    def __str__(self) -> str:
        return str(self.role)


class MyUser(AbstractUser):
    """
    Модель с пользователями
    """

    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    roles = models.ManyToManyField(Role, blank=True, serialize=True)

    def __str__(self) -> str:
        return str(self.username)


    @property
    def get_full_name(self) -> str:
        return f"{self.lastName} {self.firstName}"