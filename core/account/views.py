from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.http import HttpRequest
from .models import MyUser
from .serializers import MyUserSerializer
from .logic.users import add_users




# SECTION Обработка аккаунтов и все, что с ними связано




# NOTE Класс для обработки DELETE и PUT запросов для аккаунтов
# LINK /api/Accounts/{id}/
class MyUserViewSet(ModelViewSet):
    """
    ### Класс наследованный от ModelViewSet
    <p>Реализован для добавления такого функционала, как:</p>
    
    <ul>
        <li>Удалени пользователей по id</li>
        <li>Обновление пользователей по id</li>
    </ul>
    """

    permission_classes = [permissions.IsAdminUser, ]
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer



# NOTE класс для обработки GET и POST запросов для аккаунтов
# LINK /api/Accounts/
class MyUserAPIView(APIView):
    """
    #### Класс представления от APIView
    для вывода количества всех пользователей
    и создания новых аккаунтов
    """

    # permission_classes = [permissions.IsAdminUser,]

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