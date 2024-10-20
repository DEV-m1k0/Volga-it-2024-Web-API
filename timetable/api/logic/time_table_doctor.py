from rest_framework.response import Response
from rest_framework import status
from api.models import TimeTable, MyUser
from api.logic.users import get_users_by_role
from .date import time_to_iso8601_from_db

def get_timetable(request, id):
    try:
        response = {}

        doctor: MyUser = get_users_by_role("Doctor").get(pk=id)

        valid_tt = time_to_iso8601_from_db([doctor.time_table])

        for date in valid_tt:
            response['from'] = date[0]
            response['to'] = date[1]

        return Response(response)

    except Exception as e:
        print(e)
        return Response({
            f"ERROR_GET_TIMETABLE": f"Не удалось получить расписание для доктора. Скорее всего, доктора с id: {id} не существует!"
        }, status=status.HTTP_400_BAD_REQUEST)

def delete_time_table(id):
    try:
        response_users = get_users_by_role("Doctor")

        if response_users:
            doctor = response_users.get(pk=id)
            tt = TimeTable.objects.filter(doctorId__exact=doctor.pk)
            print(tt)
            tt.delete()
            print(tt)

        else:
            raise Exception

        return Response({f"{doctor.username}": "Записи успешно удалены!"})
    
    except Exception as e:
        print(e)
        return Response({
            f"ERROR_DOCTOR": "Расписание доктора не было удалено."
        }, status=status.HTTP_400_BAD_REQUEST)
