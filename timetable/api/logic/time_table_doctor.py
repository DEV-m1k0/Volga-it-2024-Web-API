from rest_framework.response import Response
from rest_framework import status
from api.models import TimeTable, MyUser
from api.logic.users import get_users_by_role
from .date import time_to_iso8601

def get_timetable(request, id):
    try:
        response = {}

        doctor: MyUser = get_users_by_role("Doctor").get(pk=id)

        list_by_timetables = TimeTable.objects.filter(doctorId=doctor)
        all_timetables_for_doctor = time_to_iso8601(list_by_timetables)

        for id_time_table in range(1, len(all_timetables_for_doctor)+1):
            time_table = all_timetables_for_doctor[id_time_table-1]
            response[f'{id_time_table}'] = {"from": f"{time_table[0]}",
                                            "to": f"{time_table[1]}"}

        return Response(response)

    except:
        return Response({
            f"ERROR_GET_TIMETABLE": f"Не удалось получить расписание для доктора. Скорее всего, доктора с id: {id} не существует!"
        }, status=status.HTTP_400_BAD_REQUEST)

def delete_time_table(id):
    try:
        response_users = get_users_by_role("Doctor")

        if response_users:
            doctor = response_users.get(pk=id)
            tt = TimeTable.objects.filter(doctorId__exact=doctor.pk)
            tt.delete()

        else:
            return Exception()

        return Response({f"{doctor.username}": "Записи успешно удалены!"})
    
    except:
        return Response({
            f"ERROR_DOCTOR": "Расписание доктора не было удалено. Пожалуйства, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        }, status=status.HTTP_400_BAD_REQUEST)
