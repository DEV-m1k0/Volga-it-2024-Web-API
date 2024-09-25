# SECTION - Бизнес логика для классов предствления из микросервиса account


from account.models import MyUser, ROLES, Role
from .roles import add_role
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework import status, request


# NOTE функция для добавления пользователей в базу данных
def add_users(request: HttpRequest, user: MyUser = MyUser):
    try:
        
        if isinstance(request.data, dict):
            response = add_one_user(user, request.data)

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
        response.update(add_one_user(user, user_data))

    return response



def add_one_user(user: MyUser, validated_data: dict):
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
        

def delete(request: HttpRequest, id: int):
    try:
        user = MyUser.objects.get(pk=id)
        username = str(user.username)
        user.delete()

        return Response({f"{username}": "Успешно удален"})
    
    except:
        return Response({"server": "Пользователь не найден"})


def filter_users(request: request.Request, user_role: str):
    if user_role in ROLES:
        try:
            role = Role.objects.filter(role=user_role)
            filter_users = MyUser.objects.filter(roles__in=role)
            user = filter_users[0]

            full_name: str = parse_name([user.lastName, user.firstName])

            return Response({
                "nameFilter": full_name,
                "from": user.pk,
                "count": len(filter_users)
                }, status=status.HTTP_200_OK)

        except:
            print('Ошибка при фильтрации')


def parse_name(fullName: list[str]):

    full_name_list = []

    for name in fullName:
        name1 = name.replace("('", '')
        name2 = name1.replace("',)", '')
        full_name_list.append(name2)

    return ' '.join(full_name_list)