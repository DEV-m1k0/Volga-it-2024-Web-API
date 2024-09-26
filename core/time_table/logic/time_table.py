from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from time_table.models import TimeTable
from account.models import MyUser, Role
from hospital.models import Hospital, Room
from datetime import datetime, timezone


def create_time_table(request: Request):
    try:
        
        hospitalId, doctorId, date_from, date_to, room = check_valid_data_for_time_table(request=request)

        TimeTable.objects.create(
            hospitalId=hospitalId,
            doctorId=doctorId,
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
    

def check_valid_data_for_time_table(request: Request):
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

        return hospitalId, doctorlId, date_from, date_to, room

    except:
        return False
    

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
        from_dt = datetime.strptime(request_from, '%Y-%m-%dT%H:%M:%SZ')
        to_dt = datetime.strptime(request_to, '%Y-%m-%dT%H:%M:%SZ')
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


def check_date(time_from: datetime, time_to: datetime):
    time_table_all = TimeTable.objects.all()

    for time_table in time_table_all:
        date_from_by_db = datetime.fromisoformat(str(time_table.date_from)).astimezone(timezone.utc)
        date_to_by_db = datetime.fromisoformat(str(time_table.date_to)).astimezone(timezone.utc)
        time_from_by_request = time_from.astimezone(timezone.utc)
        time_to_by_request = time_to.astimezone(timezone.utc)
        
        if (date_from_by_db <= time_from_by_request < date_to_by_db) or (date_from_by_db <= time_to_by_request <= date_to_by_db):
            return False
        
    return True


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
    

def update_time_table(request: Request, id: int) -> Response:
    try:

        time_table = TimeTable.objects.get(pk=id)

        hospitalId, doctorId, date_from, date_to, room = check_valid_data_for_time_table(request=request)

        if not check_date(time_from=date_from, time_to=date_to):
            return Response({
                "DATE_ERROR": "Запись на прием не была обновлена. Пожалуйста, убедитесь, что вы не пытаетсь обновить запись на число, которое уже занято"
            }, status=status.HTTP_400_BAD_REQUEST)

        time_table.hospitalId=hospitalId
        time_table.doctorId=doctorId
        time_table.date_from=date_from
        time_table.date_to=date_to
        time_table.room=room

        time_table.save()

        return Response({
            f"{time_table.room}": f"Запись успешшно была обновлена"
        }, status=status.HTTP_200_OK)
    
    except:
        return Response({
            "SERVER_ERROR": "Расписание не было обнавлено. Пожалуйста, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        }, status=status.HTTP_400_BAD_REQUEST)
    

def delete_time_table(request: Request, id: int) -> Response:
    try:
        time_table = TimeTable.objects.get(pk=id)
        time_table.delete()

        return Response({
            "SERVRER": "Запись была успешно удалена"
        })

    except:
        return Response({
            "SERVER_ERROR": "Расписание не было Удалено. Пожалуйста, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        }, status=status.HTTP_400_BAD_REQUEST)