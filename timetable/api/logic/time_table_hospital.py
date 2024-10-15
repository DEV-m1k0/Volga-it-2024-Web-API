from django.http.request import HttpRequest
from rest_framework.response import Response
from api.models import Hospital, TimeTable, Room
from rest_framework import status
from .date import time_to_iso8601_from_db


def delete(request: HttpRequest, id: int):
    try:
        hospital = Hospital.objects.get(pk=id)
        hospital.timetables.all().delete()

        return Response({
            f"{hospital.name}": "Расписание удалено успешно!"
        }, status=status.HTTP_200_OK)
    
    except:
        return Response({
            "SERVER_ERROR": "Больница не найдена!"
        }, status=status.HTTP_404_NOT_FOUND)
    

def get_timetable(request: HttpRequest, id: int):
    try:
        hospital = Hospital.objects.get(pk=id)
        list_dates = time_to_iso8601_from_db(hospital.timetables.all())

        response = {}

        for id_date in range(1, len(list_dates)+1):
            time_table = list_dates[id_date-1]
            response[id_date] = {
                                "from": f"{time_table[0]}",
                                "to": f"{time_table[1]}"
                                }

        return Response({
            f"{hospital.name}": response
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status": f"{e}"})
    

def get_timetable_by_room(request: HttpRequest, id: int, room: str):
    try:
        response = {}

        get_room = Room.objects.get(room=room)
        hospital = Hospital.objects.get(pk=id)

        print(get_room)
        print(hospital)

        if not get_room in hospital.rooms.all():
            return Response({
                "SERVER_ERROR": f"Комната: {room} не принадлежит больнице!"
            }, status=status.HTTP_400_BAD_REQUEST)


        list_dates = time_to_iso8601_from_db([get_room.id_timetable])

        print(list_dates)

        for id_date in range(1, len(list_dates)+1):
            time_table = list_dates[id_date-1]
            response[f'{id_date}'] = {
                                "from": f"{time_table[0]}",
                                "to": f"{time_table[1]}"
                                }

        return Response({
            f"{hospital.name}": {f"{get_room.room}": response}
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({
            "SERVER_ERROR": "Больница или комната не найдены!"
        }, status=status.HTTP_404_NOT_FOUND)