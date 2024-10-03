from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpRequest
from .models import MyUser
from .logic.users import add_users, delete, get_info
from .logic.update import update_user




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
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request: HttpRequest):
        user: MyUser = request.user

        response = get_info(user=user)

        return response
    

class UpdateMeAPIView(APIView):
    def put(self, request: Request):

        response = update_user(request)

        return response