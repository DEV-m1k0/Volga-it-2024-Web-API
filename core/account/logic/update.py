from rest_framework.response import Response
from rest_framework.request import Request
from account.models import MyUser
from .users import update_fields


def update_user(request: Request, id=False):
    if id:
        user: MyUser = MyUser.objects.get(pk=id)

        response = update_fields(user, request.data)

        return Response(response)


    else:
        user: MyUser = request.user

        response = update_fields(user, request.data)

        return Response(response)