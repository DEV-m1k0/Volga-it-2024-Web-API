from rest_framework.response import Response
from rest_framework.request import Request
from time_table.models import TimeTable
from account.models import MyUser, Role
from hospital.models import Hospital, Room
import datetime


def create_time_table(request: Request):
    try:
        if check_hospital_by_id(id=request.data["hospitalId"]):
            hospitalId = request.data["hospitalId"]

        if check_doctor_by_id(id=request.data["doctorId"]):
            doctorlId = request.data["doctorId"]

        answer, from_dt, to_dt = parse_date(request.data['from'], request.data['to'])
        if answer:
            date_from = from_dt
            date_to = to_dt

        if check_room(request.data['room']):
            room = request.data['room']

        TimeTable.objects.create(
            hospitalId=hospitalId,
            doctorlId=doctorlId,
            date_from=date_from,
            date_to=date_to,
            room=room
        )

        return Response({
            "server": "Запись успешно добавлена"
            })

    except:
        return Response({
            "SERVER_ERROR": "Расписание не было добавлено. Пожалуйства, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        })
    

def check_room(request_room: str):
    try:
        room = Room.objects.get(room=request_room)
        
        if room.room:
            return True
        
        else:
            return False

    except:
        return False


def parse_date(request_from: str, request_to: str):
    # Проверка формата дат
    try:
        from_dt = datetime.datetime.strptime(request_from, '%Y-%m-%dT%H:%M:%SZ')
        to_dt = datetime.datetime.strptime(request_to, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return False
    
    # Проверка времени от и до
    if not ((from_dt.minute % 30 == 0) and (from_dt.second == 0)):
        return False
    if not ((to_dt.minute % 30 == 0) and (to_dt.second == 0)):
        return False
    
    # Проверка интервала между датами
    if from_dt > to_dt:
        return False
    
    diff = to_dt - from_dt
    hours_diff = diff.total_seconds() / 60 ** 2

    if hours_diff <= 12:
        return True, from_dt, to_dt
    
    return False


def check_hospital_by_id(id: int):
    try:
        hospital = Hospital.objects.get(pk=id)

        if hospital.name:
            return True

        else:
            return False

    except:
        return False


def check_doctor_by_id(id: int) -> bool:
    try:
        role = Role.objects.get(role='Doctor')
        doctor = MyUser.objects.get(roles=role, pk=id)

        if doctor.roles:
            return True
        
        else:
            return False

    except:
        return False