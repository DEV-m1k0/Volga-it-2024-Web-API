from django.db import models

# Create your models here.


class Room(models.Model):
    room = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return str(self.room)
    


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contactPhone = models.CharField(max_length=11)
    rooms = models.ManyToManyField(Room, blank=True)

    def __str__(self) -> str:
        return str(self.name)
    