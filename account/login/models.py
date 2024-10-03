from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser


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
    """
    #### Модель для хранения ролей пользователей.
    """
    role = models.CharField(max_length=20)

    def __str__(self) -> str:
        return str(self.role)


class MyUser(AbstractUser):
    """
    ### Основная модель пользователей.
    Данная модель наследует от базового AbstractUser, добавляя поля:
    <ul>
        <li>lastName</li>
        <li>firstName</li>
        <li>roles</li>
    </ul>
    """

    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    roles = models.ManyToManyField(Role, blank=True, serialize=True)

    def __str__(self) -> str:
        return str(self.username)


    @property
    def get_full_name(self) -> str:
        """
        #### Свойство, возвращающее полное имя пользователя.
        """
        return f"{self.lastName} {self.firstName}"