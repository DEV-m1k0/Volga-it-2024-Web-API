


# SECTION - Бизнес логика для работы с аккаунтами пользователей из микросервиса Account



from api.models import MyUser, ROLES, Role
from .roles import add_role
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework import status, request



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
        user.roles.add(Role.objects.get(role='User'))
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


def get_all_doctors():
    try:
        role_doctor = Role.objects.get(role="Doctor")
        doctors = MyUser.objects.filter(roles=role_doctor).order_by('pk')

        return Response({
                "nameFilter": "Doctor",
                "from": doctors[0].pk,
                "count": len(doctors)
                }, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response({"SERVER": "Ошибка при получении списка врачей"})


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
        pass

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
    