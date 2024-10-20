


# SECTION - Бизнес логика для работы с расписанием больницы в микросервисе Timetable



from django.http.request import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from .date import time_to_iso8601_from_db
from api.models import Hospital, Room


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
        list_dates = time_to_iso8601_from_db([hospital.timetable])
        response = {}
        for date in list_dates:
            response['from'] = date[0]
            response['to'] = date[1]

        return Response(data=response, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"SERVER": "Скорее всего, у госпиталя еще нет расписания"})
    

def get_timetable_by_room(request: HttpRequest, id: int, room: str):
    try:
        response = {}
        get_room = Room.objects.get(room=room)
        hospital = Hospital.objects.get(pk=id)
        if not get_room in hospital.rooms.all():
            return Response({
                "SERVER_ERROR": f"Комната: {room} не принадлежит больнице!"
            }, status=status.HTTP_400_BAD_REQUEST)

        list_dates = time_to_iso8601_from_db([get_room.timetable])

        for date in list_dates:
            response['from'] = date[0]
            response['to'] = date[1]

        return Response(data=response, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({
            "SERVER_ERROR": "Больница или комната не найдены!"
        }, status=status.HTTP_404_NOT_FOUND)