from rest_framework.response import Response
from rest_framework.request import Request
from account.models import MyUser
from django.contrib.auth.hashers import make_password


def update_user(request: Request):
    user: MyUser = request.user
    
    user.lastName = request.data["lastName"]
    user.firstName = request.data["firstName"]
    user.set_password(make_password(request.data["password"]))

    print(user)

    user.save()

    return Response({"server": "Аккаунт успешно обновлен"})