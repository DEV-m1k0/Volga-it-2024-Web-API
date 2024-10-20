from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpRequest
from api.models import MyUser
from api.logic.users import *
from api.logic.update import update_user
from .serializers import *
from . import permissions



class MyUserByIdAPI(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    #### LINK: PUT /api/Accounts/{id}
    #### LINK: DELETE /api/Accounts/{id}
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser, ]

    def update(self, request: HttpRequest, id: int):
        """
        ### Изменение администратором аккаунта по id
        **body:**
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string", //имя пользователя
            "password": "string", //пароль
            "roles": [
                "string" //массив ролей пользователя
            ]
        }
        ```
        **ограничения:** Только администраторы
        """

        response = update_user(request=request, id=id)

        return response

    def destroy(self, request: HttpRequest, id: int):
        """
        ### Мягкое удаление аккаунта по id
        **ограничения:** Только администраторы
        """

        response = delete(request=request, id=id)

        return response



class MyUserAPI(generics.ListCreateAPIView):
    """
    #### LINK: GET /api/Accounts
    #### LINK: POST /api/Accounts
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser,]

    def list(self, request: HttpRequest):
        """
        ### Получение списка всех аккаунтов
        **параметры:**
        ```
        {
            "from": "int", //Начало выборки
            "count": "int" //Размер выборки
        }
        ```
        **ограничения:** Только администраторы
        """

        # проверка пользователей
        if MyUser.objects.all():
            return Response([{
                "from": MyUser.objects.all().order_by('pk')[0].pk,
                "count": len(MyUser.objects.all())
                }], status=status.HTTP_200_OK)
        
        else:
            return Response(data={
                "WARNING": "Пользователей еще нет!"
                }, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request: HttpRequest):
        """
        ### Создание администратором нового аккаунта
        **body:**
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "username": "string", //имя пользователя
            "password": "string", //пароль
            "roles": [
                "string" //массив ролей пользователя
            ]
        }
        ```
        **ограничения:** Только администраторы
        """
        
        # формирование ответа
        response = add_users(request=request)
        return response
    


class MyUserMeAPIView(generics.ListAPIView):
    """
    ### LINK: GET /api/Accounts/Me
    """
    queryset = MyUser.objects.all()
    serializer_class = GetInfoUsersSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request: HttpRequest):
        """
        ### Получение данных о текущем аккаунте
        **ограничения:** Только авторизованные пользователи
        """
        user: MyUser = request.user

        response = get_info(user=user)

        return response



class UpdateMeAPIView(generics.UpdateAPIView):
    """
    ### LINK: PUT /api/Accounts/Update
    """

    queryset = MyUser.objects.all()
    serializer_class = MyUserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, ]


    def update(self, request: Request):
        """
        ### Обновление своего аккаунта
        **body:**
        ```
        {
            "lastName": "string",
            "firstName": "string",
            "password": "string"
        }
        ```
        **ограничения:** Только авторизованные пользователи
        """

        response = update_user(request)

        return response
    


class DoctorsAPIView(generics.ListAPIView):
    """
    #### LINK: GET /api/Doctors
    """

    queryset = MyUser.objects.all()
    serializer_class = GetDoctorsSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request: Request):
        """
        ### Получение списка докторов
        **параметры:**
        ```
        {
            "nameFilter": "string" //Фильтр имени (FullName LIKE ‘%{na meFilter}%’)
            "from": "int" //Начало выборки
            "count": "int" //Размер выборки
        }
        ```
        **ограничения:** Только авторизованные пользователи
        """
        response = get_all_doctors()
        return response
    


class DoctorIdAPIView(generics.ListAPIView):
    """
    #### LINK: GET /api/Doctors/{id}
    """

    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request: Request, id: int):
        """
        ### Получение информации о докторе по Id
        **ограничения:** Только авторизованные пользователи
        """
        
        try:
            user = MyUser.objects.get(pk=id)

            response = get_info(user=user)

            return response
        
        except:
            return Response({
                "ERROR_ROLE": "Ошибка при получении ролей. Скорее всего, доктора с таким ID не существует."
                }, status=status.HTTP_400_BAD_REQUEST)