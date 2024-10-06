from .permissions import AdminOrManagerPermission
from rest_framework.request import Request
from rest_framework.views import APIView
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
    permission_classes = [AdminOrManagerPermission]

    def delete(self, request: Request, id: int):
        response = time_table_hospital.delete(request, id)
        return response