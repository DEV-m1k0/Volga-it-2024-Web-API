# SECTION - Бизнес логика для добавления аккаунтов из микросервиса authentication


from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from account.models import MyUser


def add_account(request: HttpRequest):

    data = request.data

    try:
        user = MyUser

        user.lastName = request

        return Response(data={
                "server": "Данные пришли"
            }, status=status.HTTP_200_OK)
    
    except:
        return Response(data={
                "server": "Аккаунт не создан. Пожалуйста проверьте корректность данных"
            }, status=status.HTTP_400_BAD_REQUEST)