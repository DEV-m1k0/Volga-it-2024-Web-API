from typing import Any
from .permissions import AdminOrManagerPermission
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import permissions
from .logic import time_table, time_table_doctor, time_table_hospital


# Create your views here.


class TimeTableAPIView(APIView):

    permission_classes = [AdminOrManagerPermission]

    def post(self, request: Request):
        response = time_table.create_time_table(request=request)
        return response
    
    def put(self, request: Request, id: int):
        response = time_table.update_time_table(request=request, id=id)
        return response
    
    def delete(self, request: Request, id: int):
        response = time_table.delete_time_table(id=id)
        return response
    

class TimeTableByDoctorAPIVIew(APIView):
    permission_classes = [AdminOrManagerPermission]
    def delete(self, request: Request, id: int):
        response = time_table_doctor.delete_time_table(id)
        return response
    

class TimeTableByHospitalAPIView(APIView):
    permission_classes = []
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            self.permission_classes = [AdminOrManagerPermission]
        elif request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request: Request, id: int):
        response = time_table_hospital.delete(request, id)
        return response
    
    def get(self, request: Request, id: int):
        response = time_table_hospital.get_timetable(request, id)
        return response