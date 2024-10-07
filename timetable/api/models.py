from django.db import models

# Create your models here.


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





    @property
    def get_full_name(self) -> str:
        """
        #### Свойство, возвращающее полное имя пользователя.
        """
        return f"{self.lastName} {self.firstName}"


class Room(models.Model):
    room = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return str(self.room)
    

class TimeTable(models.Model):
    hospitalId = models.PositiveIntegerField()
    doctorId = models.PositiveIntegerField()
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    room = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"from: {self.date_from} to: {self.date_to}"
    

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contactPhone = models.CharField(max_length=11)
    rooms = models.ManyToManyField(Room, blank=True)
    timetables = models.ManyToManyField(TimeTable, blank=True)

    def __str__(self) -> str:
        return str(self.name)
    

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
    time_table = models.ManyToManyField(TimeTable, blank=True)

    def __str__(self) -> str:
        return str(self.username)