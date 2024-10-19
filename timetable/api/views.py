from typing import Any
from .permissions import *
from rest_framework.request import Request
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from .logic import time_table, time_table_doctor, time_table_hospital
from .serializers import *
from .models import *


# Create your views here.


class TimeTableAPIView(generics.CreateAPIView):

    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    # permission_classes = [AdminOrManagerPermission]

    def post(self, request: Request):
        response = time_table.create_time_table(request=request)
        return response
    

class TimeTableByIdAPIView(generics.UpdateAPIView, generics.DestroyAPIView):

    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    # permission_classes = [AdminOrManagerPermission]

    def put(self, request: Request, id: int):
        response = time_table.update_time_table(request=request, id=id)
        return response
    
    def delete(self, request: Request, id: int):
        response = time_table.delete_time_table(id=id)
        return response
    

class TimeTableByDoctorAPIVIew(generics.ListAPIView, generics.DestroyAPIView):

    queryset = TimeTable.objects.all()
    serializer_class = MyUserTimeTableSerializer
    # permission_classes = []

    def despatch(self, request, *args, **kwargs):
        # if request.method == 'GET':
        #     self.permission_classes = [permissions.IsAuthenticated]
        # elif request.method == 'DELETE':
        #     self.permission_classes = [AdminOrManagerPermission]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: Request, id: int):
        response = time_table_doctor.get_timetable(request, id)
        return response

    def delete(self, request: Request, id: int):
        response = time_table_doctor.delete_time_table(id)
        return response
    

class TimeTableByHospitalAPIView(APIView):
    # permission_classes = []
    
    def dispatch(self, request, *args, **kwargs):
        # if request.method == 'DELETE':
        #     self.permission_classes = [AdminOrManagerPermission]
        # elif request.method == 'GET':
        #     self.permission_classes = [permissions.IsAuthenticated]
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request: Request, id: int):
        response = time_table_hospital.delete(request, id)
        return response
    
    def get(self, request: Request, id: int):
        response = time_table_hospital.get_timetable(request, id)
        return response
    

class TimeTableByRoomAPIView(APIView):
    # permission_classes = [AdminOrManagerOrDoctorPermission]
    def get(self, request: Request, id: int, room: str):
        response = time_table_hospital.get_timetable_by_room(request, id, room)
        return response
    
class AppointmentsByTimetableAPIView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, id: int):
        response = time_table.get_appointment(id)
        return response
    
    def post(self, request: Request, id: int):
        response = time_table.create_appointment(request, id)
        return response
    

class DeleteAppointmentByIdAPIView(APIView):
    # permission_classes = [AdminOrManagerOrPacientPermission]

    def delete(self, request: Request, id: int):
        response = time_table.delete_appointment(id)
        return response