from django.http.request import HttpRequest
from rest_framework.response import Response
from api.models import TimeTable, Hospital

def delete(request: HttpRequest, id: int):
    try:
        hospital = Hospital.objects.get(pk=id)
        hospital.timetables.all().delete()
        return Response({
            f"{hospital.name}": "Расписание удалено успешно!"
        })
    
    except:
        return Response({
            "SERVER_ERROR": "Больница не найдена!"
        })