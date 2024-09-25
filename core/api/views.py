from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import HttpRequest, Request
from account.logic.users import filter_users, get_info
from account.models import MyUser

# Create your views here.


class DoctorsAPIView(APIView):
    def get(self, request: Request):
        response = filter_users(request=request, user_role='Doctor')
        return response
    

class DoctorIdAPIView(APIView):
    def get(self, request: Request, id: int):
        
        user = MyUser.objects.get(pk=id)

        response = get_info(user=user)

        return response