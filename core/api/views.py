from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import HttpRequest, Request
from account.logic.users import filter_users

# Create your views here.


class DoctorsAPIView(APIView):
    def get(self, request: Request):
        response = filter_users(request=request, user_role='Doctor')
        return response