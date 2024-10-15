from rest_framework import serializers
from .models import *


class HistorySerializer(serializers.ModelSerializer):

    room = serializers.CharField(max_length=100)

    class Meta:
        model = History
        fields = ['date', 'pacientId', 'hospitalId', 'doctorId', 'room', 'data']
        extra_kwargs = {
            'date': {'required': True},
            'pacientId': {'required': True},
            'hospitalId': {'required': True},
            'doctorId': {'required': True},
            'room': {'required': True},
            'data': {'required': False},
        }


class HistoryAccountByIdSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100)
    roles = serializers.ListField()

    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']
        extra_kwargs = {
            'lastName': {'required': True},
            'firstName': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},
            'roles': {'required': False},
        }