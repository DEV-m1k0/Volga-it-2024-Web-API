from rest_framework import serializers
from .models import MyUser, CHOICES_ROLE_FOR_MYUSER



class MyUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователей
    """

    roles = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']