from api import models
from datetime import datetime

def validate_pacient(pacient_id: int, date: datetime) -> bool:
    try:
        pacient = models.MyUser.objects.get(pk=pacient_id)
        founded_date = pacient.appointments.get(time=date)

        if founded_date:
            return True
        return False

    except:
        return False
    

def check_hospital(hospital_id: int) -> bool:
    try:
        hospital = models.Hospital.objects.get(pk=hospital_id)

        if hospital.name:
            return True
        return False

    except:
        return False
    

def check_room(room: str, hospital_id: int) -> bool:
    try:
        founded_room = models.Room.objects.get(room=room)
        founded_hospital = models.Hospital.objects.get(pk=hospital_id)

        if founded_room in founded_hospital.rooms.all():
            return True
        return False

    except:
        return False