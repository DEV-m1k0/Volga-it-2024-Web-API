


# SECTION - Модели проекта



from django.db import models
from django.contrib.auth.models import AbstractUser



# Список ролей
CHOICES_ROLE_FOR_MYUSER = [
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('doctor', 'Doctor'),
    ('user', 'User')
]


# Возможные роли
ROLES = ['Admin', 'Manager', 'Doctor', 'User']


class Appointment(models.Model):
    """
    #### Модель для хранения информации о приёмах.
    """
    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.time}"


class Role(models.Model):
    """
    #### Модель для хранения ролей пользователей.
    """
    role = models.CharField(max_length=20)

    def __str__(self) -> str:
        return str(self.role)


class Room(models.Model):
    """
    #### Модель для хранения информации о комнатах.
    """
    room = models.CharField(max_length=50, unique=True)
    hospitals = models.ManyToManyField('Hospital', blank=True, related_name='hospitals_room')
    timetable = models.ForeignKey('TimeTable', blank=True, null=True, on_delete=models.SET_NULL, related_name='timetable_room')

    def __str__(self) -> str:
        return str(self.room)

class Hospital(models.Model):
    """
    #### Модель для хранения информации о больницах.
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contactPhone = models.CharField(max_length=11)
    rooms = models.ManyToManyField(Room, blank=True, related_name='rooms_hospital')
    timetable = models.ForeignKey('TimeTable', blank=True, null=True, on_delete=models.SET_NULL, related_name='timetable_hospital')

    def __str__(self) -> str:
        return str(self.name)
    

class MyUser(AbstractUser):
    """
    #### Основная модель для аккаунтов
    """

    roles = models.ManyToManyField(Role, blank=True, serialize=True, related_name='roles_myuser')
    appointments = models.ManyToManyField(Appointment, blank=True, related_name='appointments_myuser')
    history = models.ManyToManyField("History", blank=True, related_name='history_myuser')
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    time_table = models.ForeignKey('TimeTable', blank=True, null=True, on_delete=models.SET_NULL, related_name='time_table_myuser')

    def __str__(self) -> str:
        return str(self.username)
    
    def get_full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    
class TimeTable(models.Model):
    """
    #### Модель для хранения расписаний
    """
    hospitalId = models.ForeignKey(Hospital, blank=True, null=True, on_delete=models.SET_NULL, related_name='hospitalId_timetable')
    doctorId = models.ForeignKey(MyUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='doctorId_timetable')
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL, related_name='room_timetable')
    appointments = models.ManyToManyField(Appointment, blank=True, related_name='appointments_timetable')

    def __str__(self) -> str:
        return f"from: {self.date_from} to: {self.date_to}"
    

class History(models.Model):
    """
    #### Модель для хранения историй
    """
    date = models.DateTimeField()
    pacientId = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='pacient_history')
    hospitalId = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="hospital_history")
    doctorId = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="doctor_history")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_history")
    data = models.TextField(max_length=200)

    def __str__(self) -> str:
        if str(self.pacientId.get_full_name()):
            return f"История: {str(self.pacientId.get_full_name())}"
        
        return f"История: {self.pacientId.username}"