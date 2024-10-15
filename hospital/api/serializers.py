from rest_framework import serializers
from .models import Hospital


class HospitalSerializer(serializers.ModelSerializer):
    rooms = serializers.ListField()
    class Meta:
        model = Hospital
        fields = ['name', 'address', 'contactPhone', 'rooms']
        extra_kwargs = {
            'name': {'required': True},
            'address': {'required': True},
            'contactPhone': {'required': True},
            'rooms': {'required': False},
        }