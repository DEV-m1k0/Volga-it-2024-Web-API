from . import permissions
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .logic.hospital import (get_all, get_rooms, get_info_by_id,
                             hospital_create, update_hospital_by_id,
                             delete_hospital_by_id)
from .models import Hospital
from rest_framework import status
from rest_framework import generics
from . import serializers

# Create your views here.


class HospitalsAPIView(generics.ListCreateAPIView):

    queryset = Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: Request, id: int = False):
        response = get_all(request=request)
        return response
        
    def post(self, request: Request):

        response = hospital_create(request=request)

        return response


class HospitalByIdAPIView(generics.RetrieveUpdateDestroyAPIView, generics.ListAPIView):

    queryset = Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer
    permission_classes = [permissions.IsAdminUser]

    def dispatch(self, request, *args, **kwargs):

        if request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif request.method == 'PUT' or request.method == 'DELETE':
            self.permission_classes = [permissions.IsAdminUser]

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id, *args, **kwargs):
        response = get_info_by_id(request=request, id=id)
        return response

    def delete(self, request: Request, id: int):

        response = delete_hospital_by_id(request=request, id=id)

        return response
    
    def put(self, request: Request, id: int):
        # FIXME нужно удалять у комнаты больницу, к которой она прикреплена, если при обнавлении она убирается
        response = update_hospital_by_id(request=request, id=id)

        return response


class RoomsByIdAPIView(APIView):
    def get(self, request: Request, id: int):
        hospital = Hospital.objects.get(pk=id)
        rooms = get_rooms(hospital=hospital)

        return Response({
            "rooms": rooms
        }, status=status.HTTP_200_OK)
    
