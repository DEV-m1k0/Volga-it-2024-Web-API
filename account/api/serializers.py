from rest_framework import serializers
from .models import MyUser


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'username', 'password']
        extra_kwargs = {
            'lastName': {'required': True},
            'firstName': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},
            }