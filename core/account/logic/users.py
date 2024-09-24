# SECTION - Бизнес логика для классов предствления из микросервиса account


from account.models import MyUser
from django.contrib.auth.hashers import make_password
from .roles import add_role
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework import status


# NOTE функция для добавления пользователей в базу данных
def add_users(request: HttpRequest):
    try:
        response = {}

        for validated_data in request.data:
            user = MyUser()

            user.lastName = validated_data['lastName']
            user.firstName = validated_data['firstName']
            user.username = validated_data['username']
            user.set_password(make_password(validated_data['password']))

            user.save()

            if validated_data['roles']:
                try:
                    response_from_roles = add_role(user, validated_data)

                    response[f"{user}"] = "Пользователь успешно добавлен"

                    if response_from_roles:
                        response["messages"] = response_from_roles

                except:
                    return Response(data={
                        "server": "Роли не были добавлены"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(response)
    

    except:
        return Response(data={
            "server": 'Неверные данные'
        }, status=status.HTTP_400_BAD_REQUEST)