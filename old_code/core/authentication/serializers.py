from account.models import MyUser
from rest_framework import serializers

class SignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = ['lastName', 'firstName', 'username', 'password']