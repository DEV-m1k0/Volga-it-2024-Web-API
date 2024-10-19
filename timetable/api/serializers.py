from rest_framework import serializers
from .models import *


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['time']
        extra_kwargs = {
            'time': {'required': True},
        }


class MyUserTimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ['date_from', 'date_to']
        extra_kwargs = {
            'date_from': {'required': True},
            'date_to': {'required': True},
        }


class TimeTableSerializer(serializers.ModelSerializer):

    room = serializers.CharField(max_length=100)

    class Meta:
        model = TimeTable
        fields = ['hospitalId', 'doctorId', 'date_from', 'date_to', 'room']
        extra_kwargs = {
            'hospitalId': {'required': True},
            'doctorId': {'required': True},
            'date_from': {'required': True},
            'date_to': {'required': True},
            'room': {'required': False},
            'appointments': {'required': False}
        }