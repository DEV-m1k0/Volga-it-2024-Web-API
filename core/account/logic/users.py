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
        
        if isinstance(request.data, dict):
            response = add_one_user(request.data)

        elif isinstance(request.data, list):
            response = add_many_users(request.data)

        else:
            return Response({'data': 'Ошибка в синтаксисе json'})
                
        return Response(response)
    

    except:
        return Response(data={
            "server": 'Неверные данные'
        }, status=status.HTTP_400_BAD_REQUEST)


def add_many_users(data: list[MyUser]):
    response = {}

    for user_data in data:
        response.update(add_one_user(user_data))

    return response



def add_one_user(validated_data: dict):
    try:
        response = {}

        user = MyUser()

        user.lastName = validated_data['lastName']
        user.firstName = validated_data['firstName']
        user.username = validated_data['username']
        user.set_password(make_password(validated_data['password']))

        user.save()
    
        response[f"{user}"] = "Пользователь успешно добавлен"

        try:
            if validated_data['roles']:
                response_from_roles = add_role(user, validated_data)

                if response_from_roles:
                    response["messages"] = response_from_roles

        except:
            pass
        
        return response

    except:
        return {"server": f"{user.username} не был добавлен"}
        

    
    


