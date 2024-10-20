


# SECTION - Классы представления для микросервиса Timetable



from rest_framework.request import Request
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from .permissions import *
from .logic import time_table, time_table_doctor, time_table_hospital
from .serializers import *
from .models import *



class TimeTableAPIView(generics.CreateAPIView):
    """
    #### LINK: <u>POST /api/Timetable</u>
    """

    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [AdminOrManagerPermission]

    def post(self, request: Request):
        """
        ### Создание новой записи в расписании
        <strong>body:</strong>
        ```
        {
            "hospitalId": int,
            "doctorId": int,
            "date_from": "dateTime(ISO8601)",
            "date_to": "dateTime(ISO8601)",
            "room": "string"
        }
        ```
        <hr>
        <strong>ограничения:</strong> Только администраторы и менеджеры. {from} и {to} - количество
        минут всегда кратно 30, секунды всегда 0 (пример: “2024-04-25T11:30:00Z”, “2024-
        04-25T12:00:00Z”). {to} > {from}. Разница между {to} и {from} не должна превышать
        12 часов.
        """
        response = time_table.create_time_table(request=request)
        return response
    

class TimeTableByIdAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    #### LINK: <u>PUT /api/Timetable/{id}</u><br>
    #### LINK: <u>DELETE /api/Timetable/{id}</u><br>
    """

    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [AdminOrManagerPermission]

    def put(self, request: Request, id: int):
        """
        ### Обновление записи расписания
        <strong>body:</strong>
        ```
        {
            "hospitalId": int,
            "doctorId": int,
            "from": "dateTime(ISO8601)",
            "to": "dateTime(ISO8601)",
            "room": "string"
        }
        ```
        <hr>
        <strong>ограничения:</strong> Только администраторы и менеджеры. Нельзя изменить если есть
        записавшиеся на прием. {from} и {to} - количество минут всегда кратно 30,
        секунды всегда 0 (пример: “2024-04-25T11:30:00Z”, “2024-04-25T12:00:00Z”). {to} >
        {from}. Разница между {to} и {from} не должна превышать 12 часов.
        """

        response = time_table.update_time_table(request=request, id=id)
        return response
    
    def delete(self, request: Request, id: int):
        """
        ### Удаление записи расписания
        <strong>ограничения:</strong> Только администраторы и менеджеры
        """
        response = time_table.delete_time_table(id=id)
        return response
    

class TimeTableByDoctorAPIVIew(generics.ListAPIView, generics.DestroyAPIView):
    """
    #### LINK: <u>DELETE /api/Timetable/Doctor/{id}</u><br>
    #### LINK: <u>GET /api/Timetable/Doctor/{id}</u><br>
    """

    queryset = TimeTable.objects.all()
    serializer_class = MyUserTimeTableSerializer
    permission_classes = []

    def despatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif request.method == 'DELETE':
            self.permission_classes = [AdminOrManagerPermission]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: Request, id: int):
        """
        ### Получение расписания врача по Id
        <strong>параметры:</strong>
        ```
        {
            "from": "string(ISO8601)",
            "to": "string(ISO8601)"
        }
        ```
        <strong>ограничения:</strong> Только авторизованные пользователи
        """
        response = time_table_doctor.get_timetable(request, id)
        return response

    def delete(self, request: Request, id: int):
        """
        ### Удаление записей расписания доктора
        <strong>ограничения:</strong> Только администраторы и менеджеры
        """
        response = time_table_doctor.delete_time_table(id)
        return response
    

class TimeTableByHospitalAPIView(APIView):
    """
    #### LINK: <u>DELETE /api/Timetable/Hospital/{id}</u><br>
    #### LINK: <u>GET /api/Timetable/Hospital/{id}</u><br>
    """
    permission_classes = []
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            self.permission_classes = [AdminOrManagerPermission]
        elif request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request: Request, id: int):
        """
        ### Удаление записей расписания больницы
        <strong>ограничения:</strong> Только администраторы и менеджеры
        """
        response = time_table_hospital.delete(request, id)
        return response
    
    def get(self, request: Request, id: int):
        """
        ### Получение расписания кабинета больницы
        <strong>параметры:</strong>
        ```
        {
            "from": "string(ISO8601)",
            "to": "string(ISO8601)"
        }
        ```
        <strong>ограничения:</strong> Только администраторы и менеджеры и врачи
        """
        response = time_table_hospital.get_timetable(request, id)
        return response
    

class TimeTableByRoomAPIView(APIView):
    """
    #### LINK: GET /api/Timetable/Hospital/{id}/Room/{room}
    """
    permission_classes = [AdminOrManagerOrDoctorPermission]
    def get(self, request: Request, id: int, room: str):
        """
        ### Получение расписания кабинета больницы
        <strong>параметры:</strong>
        ```
        {
            "from": "string(ISO8601)",
            "to": "string(ISO8601)"
        }
        <strong>ограничения:</strong> Только администраторы и менеджеры и врачи
        """
        response = time_table_hospital.get_timetable_by_room(request, id, room)
        return response
    
class AppointmentsByTimetableAPIView(generics.CreateAPIView):
    """
    #### LINK: GET /api/Timetable/{id}/Appointments<br><hr>
    #### LINK: POST /api/Timetable/{id}/Appointments<br>
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, id: int):
        """
        ### Получение свободных талонов на приём.

        <strong>Детали:</strong> Каждые 30 минут из записи расписания - это один талон. Если в
        сущности Timetable from=2024-04-25T11:00:00Z, to=2024-04-25T12:30:00Z, то
        запись доступна на: 2024-04-25T11:00:00Z, 2024-04-25T11:30:00Z, 2024-04-25T12:00:00Z.<br>

        <strong>ограничения:</strong> Только авторизованные пользователи
        """
        response = time_table.get_appointment(id)
        return response
    
    def post(self, request: Request, id: int):
        """
        ### Записаться на приём
        <strong>body:</strong>
        ```
        {
            "time": "dateTime(ISO8601)"
        }
        ```
        <strong>ограничения:</strong> Только авторизованные пользователи
        """
        response = time_table.create_appointment(request, id)
        return response
    

class DeleteAppointmentByIdAPIView(APIView):
    """
    #### LINK: DELETE /api/Appointment/{id}
    """

    permission_classes = [AdminOrManagerOrPacientPermission]

    def delete(self, request: Request, id: int):
        """
        ### Отменить запись на приём
        <strong>ограничения:</strong> Только администраторы, менеджеры, и записавшийся
        пользователь
        """
        response = time_table.delete_appointment(id)
        return response