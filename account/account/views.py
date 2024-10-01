from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpRequest
from login.models import MyUser
from login.logic.users import *
from login.logic.update import update_user




# SECTION Обработка аккаунтов и все, что с ними связано




# NOTE Класс для обработки DELETE и PUT запросов для аккаунтов
# LINK /api/Accounts/{id}/
class MyUserIdAPIView(APIView):
    """
    ### Класс наследованный от ModelViewSet
    <p>Реализован для добавления такого функционала, как:</p>
    
    <ul>
        <li>Удалени пользователей по id</li>
        <li>Обновление пользователей по id</li>
    </ul>
    """

    permission_classes = [permissions.IsAdminUser, ]

    def put(self, request: HttpRequest, id: int):

        response = update_user(request=request, id=id)

        return response
    

    def delete(self, request: HttpRequest, id: int):

        response = delete(request=request, id=id)

        return response



# NOTE класс для обработки GET и POST запросов для аккаунтов
# LINK /api/Accounts/
class MyUserAPIView(APIView):
    """
    #### Класс представления от APIView
    для вывода количества всех пользователей
    и создания новых аккаунтов
    """

    permission_classes = [permissions.IsAdminUser,]

    def get(self, request: HttpRequest):
        # (GET) - рендерим запрос
        """
        ### GET запрос для класса MyUserAPIView
        
        <hr>

        <p>Если пользователи есть, то возварщает следующий <strong>GET</strong>:</p>

        {
            "from": "id 1-ого пользователя"
            "count": "Количество всех пользователей"
        }

        <hr>

        <p>Если пользователей нет, то возварщает следующий <strong>GET</strong>:</p>

        {
            "warning": "Пользователей еще нет"
        }
        """

        # проверка пользователей
        if MyUser.objects.all():
            return Response({
                "from": MyUser.objects.all()[0].pk,
                "count": len(MyUser.objects.all())
                }, status=status.HTTP_200_OK)
        
        else:
            return Response(data={
                "warning": "Пользователей еще нет"
                }, status=status.HTTP_404_NOT_FOUND)
        


    def post(self, request: HttpRequest):
        # (POST) - обработка запроса
        """
        ### POST запрос для класса MyUserAPIView

        <hr>

        <p>Если json отправлен корректный, то получим ответ в формате:</p>

        {
          "Никнейм пользователя": "Пользователь успешно добавлен"
        }

        <hr>

        <p>Если в json будет ошибка связанная с неверными ролями, то пользователь добавится,
        но роли не применятся и сервер к ответу добавит еще сообщение следующего формата:</p>
    
        {
            "massages": {
                "Никнейм пользователя": "Роли не были добавлены. Убедитесь в корректности введенных ролей"\n
            }
        }

        <hr>
        
        <p>Если в json будет ошибка, то сервер вернет следующее сообщение:</p>

        {
            "server": "Неверные данные"
        }

        """
        
        # формирование ответа
        response = add_users(request=request)
        return response
    


# NOTE класс для обработки GET запрос для аккаунта
# LINK /api/Accounts/Me/
class MyUserMeAPIView(APIView):
    """
    ### Класс для вывода информации о текущем авторизованном пользователе
    <p>Класс доступен только <strong><u>авторизованным пользователям.</u></strong></p>
    В классе реализованы следующии функции:
    <ul>
        <li>GET</li>
    </ul>
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: HttpRequest):
        """
        ### GET запрос для MyUserMeAPIView
        <hr>
        <p>Если пользователь есть, то возварщает следующий <strong>GET</strong>:</p>
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string",
            "roles": ["string"]
        }
        ```
        <hr>
        <p>Если пользователь не авторизован, то возварщает следующий <strong>GET</strong>:</p>
        ```
        {
            "ERROR_ROLE": "Ошибка при получении ролей"
        }
        ```
        """
        user: MyUser = request.user

        response = get_info(user=user)

        return response
    

class UpdateMeAPIView(APIView):
    def put(self, request: Request):

        response = update_user(request)

        return response
    

class DoctorsAPIView(APIView):
    def get(self, request: Request):
        response = filter_users(request=request, user_role='Doctor')
        return response
    

class DoctorIdAPIView(APIView):
    def get(self, request: Request, id: int):
        
        user = MyUser.objects.get(pk=id)

        response = get_info(user=user)

        return response