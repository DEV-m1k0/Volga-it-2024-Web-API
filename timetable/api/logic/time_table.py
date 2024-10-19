from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from api.models import *
from .date import *
from datetime import datetime


def create_time_table(request: Request):
    try:
        
        hospitalId, doctorId, date_from, date_to, room = check_valid_data_for_time_table(request=request)

        rooms_from_hospital = Hospital.objects.get(pk=hospitalId).rooms.all()
        if not rooms_from_hospital.filter(room=room).exists():
            return Response({
                "SERVER_ERROR": f"Комната: {room} не принадлежит больнице!"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        doctor = MyUser.objects.get(pk=doctorId)
        if doctor.time_table:
            return Response({
                "SERVER_ERROR": f"Доктор: {doctor.username} уже имеет расписание!"
            }, status=status.HTTP_400_BAD_REQUEST)

        time_table = TimeTable.objects.create(
            hospitalId=Hospital.objects.get(pk=hospitalId),
            doctorId=MyUser.objects.get(pk=doctorId),
            date_from=date_from,
            date_to=date_to,
            room=Room.objects.get(room=room)
        )
        time_table.save()

        room = Room.objects.get(room=room)
        room.timetable = time_table
        room.save()

        doctor.time_table = time_table
        doctor.save()

        hospital = time_table.hospitalId
        hospital.timetable = time_table
        hospital.save()

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

        answer, from_dt, to_dt = parse_date(request.data['date_from'], request.data['date_to'])
        if answer:
            date_from = from_dt
            date_to = to_dt

        if check_room(request.data['room']):
            room = request.data['room']

        return hospitalId, doctorlId, date_from, date_to, room

    except Exception as e:
        print(e)
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
        old_room = time_table.room

        hospitalId, doctorId, date_from, date_to, str_room = check_valid_data_for_time_table(request=request)
        if not check_date_for_room_update(room=old_room):
            return Response({
                "DATE_ERROR": "Запись на прием не была обновлена. Скорее всего, на этот прием записаны пользователи!"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        time_table.room.timetables = None
        time_table.room.save()

        time_table.hospitalId=Hospital.objects.get(pk=hospitalId)
        time_table.doctorId=MyUser.objects.get(pk=doctorId)
        time_table.date_from=date_from
        time_table.date_to=date_to
        time_table.room=Room.objects.get(room=room)
        time_table.save()

        room = Room.objects.get(room=room)
        room.timetables = time_table
        room.save()


        return Response({
            f"{time_table.room}": f"Запись успешно была обновлена"
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
            "SERVER_ERROR": "Расписание не было Удалено."
        }, status=status.HTTP_400_BAD_REQUEST)
    

def get_appointment(id: int) -> Response:
    try:
        response = {}
        appointments = Appointment.objects.all()

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

        appointments = Appointment.objects.all()

        if appointments.exists():
            for i in range(len(appointments)):
                if appointments[i].time == datetime.fromisoformat(request.data['time']):
                    raise Exception(f"Запись на этот час уже существует")
            
        if not time_table.date_from <= datetime.fromisoformat(request.data['time']) <= time_table.date_to:
            raise Exception(f"Запись на этот час не может быть создана. Она находится за диапазоном дат")


        appointment = Appointment.objects.create(
            time=request.data['time']
        )

        user = MyUser.objects.get(pk=request.user.pk)
        user.appointments.add(appointment)
        user.save()

        time_table.appointments.add(appointment)
        time_table.save()

        return Response({
            "SERVER": "Запись успешно добавлена"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({
            "SERVER_ERROR": f"Запись не была добавлена! {e}"
        }, status=status.HTTP_400_BAD_REQUEST)
    

def delete_appointment(id: int) -> Response:
    try:
        appointment = Appointment.objects.get(pk=id)
        appointment.delete()

        return Response({
            "SERVRER": "Запись была успешно удалена"
        })

    except:
        return Response({
            "SERVER_ERROR": "Запись не была удалена. Скорее всего, такой записи нет"
        }, status=status.HTTP_400_BAD_REQUEST)