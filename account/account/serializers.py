from rest_framework import serializers
from api.models import *


class MyUserUpdateSerializer(serializers.ModelSerializer):

    lastName = serializers.CharField(max_length=100)
    firstName = serializers.CharField(max_length=100)

    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'password']
        extra_kwargs = {
            'lastName': {'required': True},
            'firstName': {'required': True},
            'password': {'required': True, 'write_only': True},
        }

    def update(self, instance, validated_data):
        print(validated_data)
        return super().update(instance, validated_data)