from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.request import Request, HttpRequest
from rest_framework.status import HTTP_205_RESET_CONTENT
from account.logic.users import add_one_user


#SECTION - Регистрация пользователей и получение токенов


class SignUpAPIView(APIView):
    def post(self, request: Request):

        response = add_one_user(request.data)

        return Response(response)


class ValidateTokenAPIView(APIView):
    def get(self, request: Request):
        return Response({"accessToken": f"{request.user.access_token}"})
    


#SECTION - Занесение токенов в BlackList


from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


class ResetTokenAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request: HttpRequest):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        user = request.user
        
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(data={
            f"{user}": "Успешно вышел"
        }, status=HTTP_205_RESET_CONTENT)
    

