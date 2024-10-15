from rest_framework import serializers
from api.models import *


class UpdateUserByIdSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100)
    roles = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']


class GetUsersSerializer(serializers.Serializer):
    From = serializers.IntegerField()
    count = serializers.IntegerField()


class GetDoctorsSerializer(serializers.Serializer):
    nameFilter = serializers.CharField(max_length=100)
    From = serializers.IntegerField()
    count = serializers.IntegerField()

class GetInfoUsersSerializer(serializers.ModelSerializer):

    roles = serializers.ListField()
    username = serializers.CharField(max_length=100)

    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'username', 'roles']


class MyUserSerializer(serializers.ModelSerializer):

    roles = serializers.ListField()
    username = serializers.CharField(max_length=100)

    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']
        extra_kwargs = {
            'lastName': {'required': True},
            'firstName': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},
            'roles': {'required': False}
        }


class PostUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all())
    
    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'username', 'password', 'roles']
        extra_kwargs = {
            'lastName': {'required': True},
            'firstName': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},
            'roles': {'required': False}
        }


class MyUserUpdateSerializer(serializers.ModelSerializer):
    roles = serializers.ListField()
    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'password', 'roles']
        extra_kwargs = {
            'lastName': {'required': True},
            'firstName': {'required': True},
            'password': {'required': True, 'write_only': True},
            'roles': {'required': False}
        }