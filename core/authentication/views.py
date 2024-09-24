from rest_framework.views import APIView
from rest_framework.response import Response
from .logic.account import add_account
from account.logic.users import add_one_user


class SignUpAPIView(APIView):
    def post(self, request):

        response = add_one_user(request.data)

        return Response(response)