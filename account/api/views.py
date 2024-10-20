from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.request import Request, HttpRequest
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .logic.users import add_users
from rest_framework import generics
from .models import MyUser
from .serializers import *


#SECTION - Регистрация пользователей и получение токенов


# LINK /api/Authentication/SignUp/
class SignUpAPIView(generics.CreateAPIView):
    """
    #### LINK: POST /api/Authentication/SignUp
    """
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request: Request):
        """
        ### Регистрация нового аккаунта
        **body:**
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string",
            "password": "string"
        }
        ```
        **ограничения:** Нет
        """

        response = add_users(request)

        return response


# LINK /api/Authentication/Validate/
class ValidateTokenAPIView(APIView):
    """
    #### GET /api/Authentication/Validate
    """
    def get(self, request: Request):
        """
        ### Интроспекция токена
        **параметры:**
        ```
        {
            "accessToken": "string"
        }
        ```
        **ограничения:** Нет
        """
        try:
            token = request.headers.get('Authorization').split(' ')[1]  # Достаем токен из заголовка
            return Response({"accessToken": f"{token}"})
        except Exception as e:
            return Response({"TOKEN_ERROR": f"Токен не активен: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    

class ResetTokenAPIView(APIView):
    """
    #### LINK: PUT /api/Authentication/SignOut
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def put(self, request: HttpRequest):
        """
        ### Выход из аккаунта
        **ограничения:** Только авторизованные пользователи
        """
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        user = request.user
        
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(data={
            f"{user}": "Успешно вышел"
        }, status=status.HTTP_200_OK)
    

