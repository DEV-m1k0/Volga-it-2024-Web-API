from rest_framework.views import APIView
from rest_framework import status, mixins
from rest_framework.response import Response
from . import permissions
from rest_framework.request import Request
from django.http import HttpRequest
from api.models import MyUser
from api.logic.users import *
from api.logic.update import update_user
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import generics



# SECTION Обработка аккаунтов и все, что с ними связано



# LINK /api/Accounts/{id}/
class MyUserByIdAPI(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    ### Класс для работы с пользователем по id.
    <p>Данный класс доступен только администраторам.</p>
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser, ]

    def update(self, request: HttpRequest, id: int):
        """
        ### PUT запрос для класса MyUserIdAPIView.
        <p>Используется для изменения информации о пользователе.</p>
        <p>Если данные будут валиндны, тогда сервер вернет:</p>
        ```
        {
            "username": "Успешно обновлен"
        }
        ```
        <hr>
        <p>Если в json будут некорректные роли, а все остальные данные будут валидны, тогда сервер вернет:</p>
        ```
        {
            "username": "Успешно обновлен",
            "messages": {
                "username": "Роли не были добавлены. Убедитесь в корректности введенных ролей"
            }
        }
        ```
        <hr>
        <p>Если в синтаксисе json будет ошибка, то сервер вернет следующий ответ:</p>
        ```
        {
            "ERROR_username": "Пользователь не был обновлен. Пожалуйста, проверьте корректность json"
        }
        ```
        """

        response = update_user(request=request, id=id)

        return response

    def destroy(self, request: HttpRequest, id: int):
        """
        ### DELETE запрос для класса MyUserIdAPIView.
        <p>Используется для удаления пользователя.</p>
        <p>Если пользователь будет успешно удален, сервер вернет:</p>
        ```
        {
            "username": "Успешно удален"
        }
        ```
        <hr>
        <p>Если пользователь не найден, то сервер вернет:</p>
        ```
        {
            "SERVER_NOT_FOUND": "Пользователь не найден"
        }
        ```
        """

        response = delete(request=request, id=id)

        return response

# LINK /api/Accounts/
class MyUserAPI(generics.ListCreateAPIView):
    """
    ### Класс для вывода количества всех пользователей.
    <p>Данный класс доступен только администраторам.</p>
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser,]

    def list(self, request: HttpRequest):
        """
        ### GET запрос для класса MyUserAPIView
        <p>Если вы пытаетесь получить доступ через аккаунт, у которого нет прав администратора, то будет получен следующий ответ:</p>
        ```
        {
            "detail": "У вас недостаточно прав для выполнения данного действия."
        }
        ```
        <hr>
        <p>Если пользователи есть, то возварщает следующий ответ:</p>
        ```
        {
            "from": "id 1-ого пользователя"
            "count": "Количество всех пользователей"
        }
        ```
        <hr>
        <p>Если пользователей нет, то возварщает следующий ответ:</p>
        ```
        {
            "WARNING": "Пользователей еще нет!"
        }
        ```
        """

        # проверка пользователей
        if MyUser.objects.all():
            return Response([{
                "from": MyUser.objects.all()[0].pk,
                "count": len(MyUser.objects.all())
                }], status=status.HTTP_200_OK)
        
        else:
            return Response(data={
                "WARNING": "Пользователей еще нет!"
                }, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request: HttpRequest):
        """
        ### POST запрос для класса MyUserAPIView
        Данный метод поддержит обработку POST запроса для добавления одного или нескольких пользователей.
        <p>Если json отправлен корректный, то получим ответ в формате:</p>
        ```
        {
          "username": "Пользователь успешно добавлен"
        }
        ```
        <hr>
        <p>Если в json будет ошибка связанная с неверными ролями, то пользователь добавится,
        но роли не применятся и сервер к ответу добавит еще сообщение следующего формата:</p>
        ```
        {
            "username": "Пользователь успешно добавлен",
            "messages": {
                "username": "Роли не были добавлены. Убедитесь в корректности введенных ролей"
            }
        }
        ```
        <hr>
        <p>Если в синтаксисе json будет ошибка, то сервер вернет следующее сообщение:</p>
        ```
        {
            "DATA_ERROR": "Данные некорректны. Пожалуйста, убедитесь, что json корректен!"
        }
        ```
        <hr>
        <p>Если вы попытаетесь добавить пользователя с пустым паролем, то сервер вернет следующий результат:</p>
        ```
        {
            "username_PASSWORD_ERROR": "Пароль не может быть пустым!"
        }
        ```
        """
        
        # формирование ответа
        response = add_users(request=request)
        return response
    

from rest_framework import generics

# LINK /api/Accounts/Me/
class MyUserMeAPIView(generics.ListAPIView):
    """
    ### Класс для вывода информации о текущем авторизованном пользователе
    <p>Класс доступен только <strong><u>авторизованным пользователям.</u></strong></p>
    В классе реализованы следующии функции:
    <ul>
        <li>GET</li>
    </ul>
    """
    queryset = MyUser.objects.all()
    serializer_class = GetInfoUsersSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request: HttpRequest):
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



# LINK /api/Accounts/Update/
class UpdateMeAPIView(generics.UpdateAPIView):
    """
    ### Класс для изменения информации текущего авторизованного пользователя
    <p>Класс доступен только <strong><u>авторизованным пользователям.</u></strong></p>
    В классе реализованы следующие методы:
    <ul>
        <li>PUT</li>
    </ul>
    """

    queryset = MyUser.objects.all()
    serializer_class = MyUserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, ]


    def update(self, request: Request):
        """
        ### PUT запрос для UpdateMeAPIView
        <p>Метод принимает json с новыми данными пользователя и сохраняет их в БД.</p>
        Поддерживается следующий формат json:
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "password": "string"
        }
        ```
        <p>Если данные корректны, то возвращает следующий ответ:</p>
        ```
        {
            "username": "Успешно обновлен"
        }        
        ```
        <p>Если данные не корректны, то будет возвращено следующие искючение:</p>
        ```
        {
            "username": "Пользователь не был обновлен. Пожалуйста, проверьте корректность json"
        }
        ```
        """

        response = update_user(request)

        return response
    



# SECTION для работы с докторами


# LINK /api/Doctors/
class DoctorsAPIView(generics.ListAPIView):
    """
    ### Класс для вывода списка всех докторов.
    <p>Класс доступен только авторизованным пользователям.</p>
    В данном классе реализованы следующие методы:
    <ul>
        <li>GET</li>
    </ul>
    """

    queryset = MyUser.objects.all()
    serializer_class = GetDoctorsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request: Request):
        """
        ### GET запрос для DoctorsAPIView.
        <p>При вызове данного метода, если пользователи с ролью 'Doctor' будут найдены, то сервер вернет:</p>
        ```
        {
            "nameFilter": "Полное имя первого найденного доктора",
            "from": "ID первого доктора",
            "count": "Количество всех докторов"
        }
        ```
        <hr>
        <p>Если пользователей с ролью 'Doctor' не будет, то сервер вернет:</p>
        ```
        {
            "SERVER_NOT_FOUND": "Сервер не нашел пользователей с данной ролью. Скорее всего, пользователь с такой ролью не существует."
        }
        ```
        """
        response = filter_users(request=request, user_role='Doctor')
        return response
    

# LINK /api/Doctors/{id}/
class DoctorIdAPIView(generics.ListAPIView):
    """
    ### Класс для получения информации о докторе по ID.
    <p>Данный класс доступен только для авторизованных пользователей</p>
    <p>В класс реализованы следующие методы:</p>
    <ul>
        <li>GET</li>
    </ul>
    """

    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request: Request, id: int):
        """
        ### GET запрос для DoctorIdAPIView.
        <p>В данном методе мы получаем ID доктора. Если доктор с таким ID существует, то сервер возваращает:</p>
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string",
            "roles": [
                "string",
                ...,
                "string",
            ]
        }
        ```
        <p>Если доктора с таким ID не существует, тогда сервер возвращает:</p>
        ```
        {
            "ERROR_ROLE": "Ошибка при получении ролей. Скорее всего, доктора с таким ID не существует."
        }
        ```
        """
        
        try:
            user = MyUser.objects.get(pk=id)

            response = get_info(user=user)

            return response
        
        except:
            return Response({
                "ERROR_ROLE": "Ошибка при получении ролей. Скорее всего, доктора с таким ID не существует."
                }, status=status.HTTP_400_BAD_REQUEST)