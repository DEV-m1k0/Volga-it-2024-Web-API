# SECTION - Бизнес логика для классов предствления из микросервиса account


from ..models import MyUser, ROLES, Role
from .roles import add_role
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework import status, request


# NOTE функция для добавления пользователей в базу данных
def add_users(request: HttpRequest, user: MyUser = MyUser):
    try:
        
        if isinstance(request.data, dict):
            if request.data['password'] == "":
                return Response(
                    {"USER_PASSWORD_ERROR": "Пароль не может быть пустым!"},
                    status=status.HTTP_400_BAD_REQUEST)
            response = add_one_user(user, request.data)

        elif isinstance(request.data, list):
            response = add_many_users(request.data)
        
        return Response(response, status=status.HTTP_207_MULTI_STATUS)
    

    except:
        return Response(data={
            "DATA_ERROR": 'Данные некорректны. Пожалуйста, убедитесь, что json корректен!'
        }, status=status.HTTP_400_BAD_REQUEST)


def add_many_users(data: list[MyUser]):
    response = {}

    for user_data in data:
        user = MyUser
        response.update(add_one_user(user, user_data))

    return response


def add_one_user(user: MyUser, validated_data: dict):
    try:
        if validated_data['password'] == "":
            return {f"{validated_data['username']}_PASSWORD_ERROR": "Пароль не может быть пустым!"}
        
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
            response[f"{user.username}_messages"] = "Ошибка при добавлении ролей. Скорее всего, ошибка в синтаксисе!"
            return response
        
        return response

    except:
        return {f"{validated_data['username']}_USER_ERROR": "Пользователь не был добавлен. Скорее всего, пользователь с таким username уже существует или какое-то из полей написано не вернно!"}
        

def delete(request: HttpRequest, id: int):
    try:
        user = MyUser.objects.get(pk=id)
        username = str(user.username)
        user.delete()

        return Response({f"{username}": "Успешно удален"}, status=status.HTTP_200_OK)
    
    except:
        return Response({"SERVER_NOT_FOUND": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


def filter_users(request: request.Request, user_role: str):
    if user_role in ROLES:
        try:
            role = Role.objects.filter(role=user_role)
            filter_users = MyUser.objects.filter(roles__in=role)
            user = filter_users[0]

            return Response({
                "nameFilter": user.get_full_name,
                "from": user.pk,
                "count": len(filter_users)
                }, status=status.HTTP_200_OK)

        except:
            print('Ошибка при фильтрации')


def get_info(user: MyUser):

    role_list = []
    try:
        for role in user.roles.all():
            role_list.append(role.role)

    except:
        return Response({"ERROR_ROLE": "Ошибка при получении ролей"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "lastName": str(user.lastName),
        "firstName": str(user.firstName),
        "username": str(user.username),
        "roles": role_list
        })


def get_users_by_role(request_role: str):
    try:
        role = Role.objects.get(role="Doctor")
        users = MyUser.objects.filter(roles__exact=role)

        return users

    except:
        print(False)
        return False
    