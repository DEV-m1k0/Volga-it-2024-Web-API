from api import models
from datetime import datetime
from .date import parse_one_date

def check_doctor(id):
    try:
        doctor = models.MyUser.objects.get(pk=id)

        if doctor.roles.all().get(role='Doctor'):
            return True
        return False
    
    except:
        return False


def check_data(data: dict) -> bool:
    try:
        if 'pacientId' not in data or 'hospitalId' not in data or 'doctorId' not in data or 'room' not in data or 'date' not in data or 'data' not in data:
            return False
        answer, _ = parse_one_date(data['date'])
        return answer
    except:
        return False

def validate_pacient(pacient_id: int, date: datetime) -> bool:
    try:
        pacient = models.MyUser.objects.get(pk=pacient_id)
        founded_date = pacient.appointments.get(time=date)

        if founded_date:
            return True
        return False

    except:
        return False
    

def check_pacient(id: int) -> bool:
    try:
        pacient = models.MyUser.objects.get(pk=id)

        if pacient.appointments.exists():
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