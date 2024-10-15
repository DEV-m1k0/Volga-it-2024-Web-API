from rest_framework.response import Response
from rest_framework.request import Request
from api.models import MyUser
from .roles import add_role


def update_user(request: Request, id=False):
    if id:
        user: MyUser = MyUser.objects.get(pk=id)

        response = update(user, request.data)

        return Response(response)


    else:
        user: MyUser = request.user

        response = update(user, request.data)

        return Response(response)
    

def update(user: MyUser, data) -> dict:
    try:
        response = {}

        user.lastName=data['lastName']
        user.firstName=data['firstName']

        try:
            user.username=data['username']
        except:
            pass

        user.set_password(data['password'])

        user.save()

        response[f"{user.username}"] = "Успешно обновлен"

        try:
            if data['roles']:
                response_from_roles = add_role(user, data)

                if response_from_roles:
                    response["messages"] = response_from_roles

        except:
            response["messages"] = "Роли не были добавлены"

        return response
    
    except:
        return {f"{user.username}": "Пользователь не был обновлен. Пожалуйста, проверьте корректность json"}