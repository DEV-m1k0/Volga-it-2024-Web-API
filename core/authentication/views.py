from rest_framework.views import APIView
from .logic.account import add_account


class SignUpAPIView(APIView):
    def post(self, request):

        response = add_account(request)

        return response 