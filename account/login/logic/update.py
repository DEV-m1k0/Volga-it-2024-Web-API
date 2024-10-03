from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from ..models import MyUser
from .roles import add_role



def update_user(request: Request, id=False):
    if id:
        user: MyUser = MyUser.objects.get(pk=id)
        response = update(user, request.data)

        if f"ERROR_{user.username}" in response.keys():
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)


    else:
        user: MyUser = request.user
        response = update(user, request.data)

        if f"ERROR_{user.username}" in response.keys():
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status=status.HTTP_200_OK)
    

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
            pass

        return response
    
    except:
        return {f"ERROR_{user.username}": "Пользователь не был обновлен. Пожалуйста, проверьте корректность json"}