from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from api.models import *
from .date import (check_date, parse_date, time_to_iso8601_from_db,
                   get_appointments, time_to_iso8601)
from datetime import datetime


def create_time_table(request: Request):
    try:
        
        hospitalId, doctorId, date_from, date_to, room = check_valid_data_for_time_table(request=request)

        if not check_date(date_from, date_to):
            return Response({
                "SERVER_ERROR": "Некорректные даты!"
            }, status=status.HTTP_400_BAD_REQUEST)

        time_table = TimeTable.objects.create(
            hospitalId=Hospital.objects.get(pk=hospitalId),
            doctorId=MyUser.objects.get(pk=doctorId),
            date_from=date_from,
            date_to=date_to,
            id_room=Room.objects.get(room=room)
        )

        hospital = Hospital.objects.get(pk=hospitalId)
        hospital.timetables.add(time_table)
        hospital.save()

        room = Room.objects.get(room=room)
        room.timetables.add(time_table)

        return Response({
            "server": "Запись успешно добавлена"
            }, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({
            "SERVER_ERROR": "Расписание не было добавлено. Пожалуйства, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        }, status=status.HTTP_400_BAD_REQUEST)
    

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

        room = Room.objects.get(room=request.data['room'])

        if not Hospital.objects.filter(pk=request.data['hospitalId'], rooms=room).exists():
            raise Exception(f"Комната {request.data['room']} в данной больнице не найдена")

        time_table = TimeTable.objects.get(pk=id)

        time_table.id_room.timetables.remove(time_table)

        hospitalId, doctorId, date_from, date_to, room = check_valid_data_for_time_table(request=request)
        if not check_date(time_from=date_from, time_to=date_to):
            return Response({
                "DATE_ERROR": "Запись на прием не была обновлена. Пожалуйста, убедитесь, что вы не пытаетсь обновить запись на число, которое уже занято"
            }, status=status.HTTP_400_BAD_REQUEST)

        time_table.hospitalId=Hospital.objects.get(pk=hospitalId)
        time_table.doctorId=MyUser.objects.get(pk=doctorId)
        time_table.date_from=date_from
        time_table.date_to=date_to
        time_table.id_room=Room.objects.get(room=room)

        Room.objects.get(room=time_table.id_room).timetables.remove(time_table)

        room = Room.objects.get(room=room)
        room.timetables.add(time_table)

        time_table.save()

        return Response({
            f"{time_table.id_room}": f"Запись успешно была обновлена"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({
            "SERVER_ERROR": f"Расписание не было обнавлено!"
        }, status=status.HTTP_400_BAD_REQUEST)
    

def delete_time_table(id: int) -> Response:
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
    

def get_appointment(id: int) -> Response:
    try:
        response = {}
        appointments = Apointment.objects.all()

        if appointments.exists():
            for i in range(len(appointments)):
                response[f"Талончик {i+1}"] = appointments[i].time

        else:
            return Response({
                "WARNING": "Талончиков еще нет!"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "Рассписание": response
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({
            "SERVER_ERROR": "Запись с расписанием не найдена!"
        }, status=status.HTTP_400_BAD_REQUEST)
    

def create_appointment(request: Request, timetable_id: int) -> Response:
    try:
        time_tables = TimeTable.objects.filter(pk=timetable_id)
        time_table = time_tables[0]

        if not time_tables.exists():
            raise Exception(f"Расписание с id {timetable_id} не найдено")

        appointments = Apointment.objects.all()

        print(time_table.date_from)
        print(time_table.date_to)

        
        if appointments.exists():
            for i in range(len(appointments)):
                if appointments[i].time == datetime.fromisoformat(request.data['time']):
                    raise Exception(f"Запись на этот час уже существует")
            
        if not time_table.date_from <= datetime.fromisoformat(request.data['time']) <= time_table.date_to:
            raise Exception(f"Запись на этот час не может быть создана. Она находится за диапазоном дат")


        Apointment.objects.create(
            time=request.data['time']
        )
        return Response({
            f"": f"Запись успешно добавлена"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({
            "SERVER_ERROR": f"Запись не была добавлена! {e}"
        }, status=status.HTTP_400_BAD_REQUEST)