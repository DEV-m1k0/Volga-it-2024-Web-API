


# SECTION - Классы предстваления для микросервиса Document



from rest_framework import generics
from .logic import history
from .permissions import *
from . import serializers
from .models import *



class HistoryByIdAPIView(generics.ListAPIView, generics.UpdateAPIView):
    """
    #### LINK: GET /api/History/{id}
    #### LINK: PUT /api/History/{id}
    """
    queryset = History.objects.all()
    serializer_class = serializers.HistorySerializer
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.permission_classes = [DoctorOrPacientPermission]
        elif request.method == "PUT":
            self.permission_classes = [AdminOrManagerOrDoctorPermission]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        """
        ### Получение подробной информации о посещении и назначениях
        <strong>ограничения:</strong> Только врачи и аккаунт, которому принадлежит история
        """
        response = history.get_history(id)
        return response
    
    def put(self, request, id):
        """
        ### Обновление истории посещения и назначения
        <strong>body:</strong>
        ```
        {
            "date": "dateTime(ISO8601)",
            "pacientId": int,
            "hospitalId": int,
            "doctorId": int,
            "room": "string",
            "data": "string"
        }
        ```
        <strong>ограничения:</strong> Только администраторы и менеджеры и врачи. {pacientId} - с
        ролью User.
        """
        response = history.put_history(request, id)
        return response
    


class HistoryAPI(generics.CreateAPIView):
    """
    #### LINK: POST /api/History
    """
    queryset = History.objects.all()
    serializer_class = serializers.HistorySerializer
    permission_classes = [AdminOrManagerOrDoctorPermission]
    def post(self, request):
        """
        ### Создание истории посещения и назначения
        <strong>body:</strong>
        ```
        {
            "date": "dateTime(ISO8601)",
            "pacientId": int,
            "hospitalId": int,
            "doctorId": int,
            "room": "string",
            "data": "string"
        }
        ```
        <strong>ограничения:</strong> Только администраторы и менеджеры и врачи. {pacientId} - с
        ролью User.
        """
        response = history.post_history(request)
        return response


class HistoryPacientAPIView(generics.ListAPIView):
    """
    #### LINK: GET /api/History/Account/{id}
    """
    queryset = history.History.objects.all()
    permission_classes = [DoctorOrPacientPermission]
    def get(self, request, id):
        """
        ### Получение истории посещений и назначений аккаунта
        <strong>Пример ответа сервера на валидный запрос:</strong><br>
        ```
        {
            "История: firstName lastName": {
                "int": {
                    "id": int,
                    "pacientId": int,
                    "hospitalId": int,
                    "doctorId": int,
                    "room": "string",
                    "date": "dateTime(ISO8601)",
                    "data": "string"
                }
            }
        }
        ```
        <strong>ограничения:</strong> Только врачи и аккаунт, которому принадлежит история
        """
        response = history.get_history_by_pacient(id)
        return response