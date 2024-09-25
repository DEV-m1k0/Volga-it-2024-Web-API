from django.db import models
from hospital.models import Hospital



# Create your models here.

class TimeTable(models.Model):
    hospitalId = models.PositiveIntegerField()
    doctorlId = models.PositiveIntegerField()
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    room = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"from: {self.date_from} to: {self.date_to}"