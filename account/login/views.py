import jwt.algorithms
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.request import Request, HttpRequest
from rest_framework import status
from rest_framework_simplejwt.tokens import Token
from .logic.users import add_users
from login.models import MyUser


#SECTION - Регистрация пользователей и получение токенов


class SignUpAPIView(APIView):
    """
    ### Класс для регистрации пользователей
    """
    def post(self, request: Request):
        """
        ### POST запрос для класса SignUpAPIView.
        <p>Если данные корректны, добавляет нового пользователя в БД.</p>
        <p>Если данные некорректны, возвращает ошибку с описанием причины ошибки.</p>
        <p>Формат json запроса: POST /api/Authentication/SignUp/ может принимать как list так и dict с полями: lastName, firstName, username, password.</p>
        <hr>
        <p>Пример допустимых форматов json:</p>
        <h3>dict:</h3>
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string",
            "password": "string"
        }
        ```
        <br>
        <h3>list:</h3>
        ```
        [
            {
                "lastName": "string",
                "firstName": "string",
                "username": "string",
                "password": "string"
            },
            {
                "lastName": "string",
                "firstName": "string",
                "username": "string",
                "password": "string"
            }
        ]
        ```
        """

        response = add_users(request)

        return response


class ValidateTokenAPIView(APIView):
    """
    ### Класс для интроспекции токена
    В классе реализованы следующие методы:
    <ul>
        <li>GET</li>
    </ul>
    """
    def get(self, request: Request):
        """
        ### GET запрос для класса ValidateTokenAPIView
        Если токен активен, возвращает его.\n
        Если токен не активен, возвращает исключение.
        """
        try:
            token = request.headers.get('Authorization').split(' ')[1]  # Достаем токен из заголовка
            return Response({"accessToken": f"{token}"})
        except Exception as e:
            return Response({"TOKEN_ERROR": f"Токен не активен: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    


#SECTION - Занесение токенов в BlackList


from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


class ResetTokenAPIView(APIView):
    """
    ### Класс для сброса токенов
    <p>Этот класс доступен только для авторизованных пользователей.</p>
    В классе реализованы следующие методы:
    <ul>
        <li>PUT</li>
    </ul>
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def put(self, request: HttpRequest):
        """
        ### PUT запрос для класса ResetTokenAPIView
        <p>Сбрасывает все токены пользователя в черный список.</p>
        """
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        user = request.user
        
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(data={
            f"{user}": "Успешно вышел"
        }, status=status.HTTP_200_OK)
    

