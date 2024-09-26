from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import TimeTable
from .logic.time_table import create_time_table, update_time_table


# Create your views here.


class TimeTableAPIView(APIView):
    def post(self, request: Request):
        response = create_time_table(request=request)
        return response
    
    def put(self, request: Request, id: int):
        response = update_time_table(request=request, id=id)
        return response