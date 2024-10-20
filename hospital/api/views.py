


# SECTION - Классы предстваления для микросервиса Hospital



from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .logic.hospital import *
from .models import Hospital
from . import permissions
from . import serializers



class HospitalsAPIView(generics.ListCreateAPIView):
    """
    #### LINK: GET /api/Hospitals
    #### LINK: POST /api/Hospitals
    """

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
        """
        ### Получение списка больниц
        **параметры:**
        ```
        {
            "from": "int", //Начало выборки
            "count": "int" //Размер выборки
        }
        ```
        **ограничения:** Только авторизованные пользователи
        """
        response = get_all(request=request)
        return response
        
    def post(self, request: Request):
        """
        ### Создание записи о новой больнице
        **body:**
        ```
        {
            "name": "string",
            "address": "string",
            "contactPhone": "string",
            "rooms": [
                "string" //массив наименований кабинетов
            ]
        }
        ```
        **ограничения:** Только администраторы
        """
        response = hospital_create(request=request)

        return response



class HospitalByIdAPIView(generics.RetrieveUpdateDestroyAPIView, generics.ListAPIView):
    """
    #### LINK: GET /api/Hospitals/{id}
    #### LINK: PUT /api/Hospitals/{id}
    #### LINK: DELETE /api/Hospitals/{id}
    """

    queryset = Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif request.method == 'PUT' or request.method == 'DELETE':
            self.permission_classes = [permissions.IsAdminUser]

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id, *args, **kwargs):
        """
        ### Получение информации о больнице по Id
        **ограничения:** Только авторизованные пользователи
        """
        response = get_info_by_id(request=request, id=id)
        return response

    def delete(self, request: Request, id: int):
        """
        ### Мягкое удаление записи о больнице
        **ограничения:** Только администраторы
        """
        response = delete_hospital_by_id(request=request, id=id)

        return response
    
    def put(self, request: Request, id: int):
        """
        ### Изменение информации о больнице по Id
        **body:**
        ```
        {
            "name": "string",
            "address": "string",
            "contactPhone": "string",
            "rooms": [
                "string" //массив наименований кабинетов
            ]
        }
        ```
        **ограничения:** Только администраторы
        """
        response = update_hospital_by_id(request=request, id=id)

        return response



class RoomsByIdAPIView(APIView):
    """
    #### LINK: GET /api/Hospitals/{id}/Rooms
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request: Request, id: int):
        """
        ### Получение списка кабинетов больницы по Id
        **ограничения:** Только авторизованные пользователи
        """
        hospital = Hospital.objects.get(pk=id)
        rooms = get_rooms(hospital=hospital)

        return Response({
            "rooms": rooms
        }, status=status.HTTP_200_OK)
    
