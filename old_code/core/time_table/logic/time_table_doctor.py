from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from time_table.models import TimeTable
from account.models import MyUser, Role
from hospital.models import Hospital, Room
from datetime import datetime, timezone
from account.logic.users import get_users_by_role


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
        })
