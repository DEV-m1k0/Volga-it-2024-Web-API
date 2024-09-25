# SECTION - Бизнес логика для классов предствления из микросервиса account


from account.models import MyUser
from .roles import add_role
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework import status


# NOTE функция для добавления пользователей в базу данных
def add_users(request: HttpRequest, user: MyUser = MyUser):
    try:
        
        if isinstance(request.data, dict):
            response = update_fields(user, request.data)

        elif isinstance(request.data, list):
            response = add_many_users(request.data)

        else:
            return Response({'Server': 'Ошибка в синтаксисе json'})
                
        return Response(response)
    

    except:
        return Response(data={
            "server": 'Неверные данные'
        }, status=status.HTTP_400_BAD_REQUEST)


def add_many_users(data: list[MyUser]):
    response = {}

    for user_data in data:
        user = MyUser
        response.update(update_fields(user, user_data))

    return response



def update_fields(user: MyUser, validated_data: dict):
    try:
        response = {}

        user = user.objects.create(
             lastName=validated_data['lastName'],
             firstName=validated_data['firstName'],
             username=validated_data['username']
             )

        user.set_password(validated_data['password'])

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
        return {f"{user.username}": "не был добавлен"}
        

    
    


