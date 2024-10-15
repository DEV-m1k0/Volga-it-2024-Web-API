from rest_framework.views import APIView
from rest_framework import generics
from .logic import history
from .permissions import *
from . import serializers
from .models import *


# Create your views here.

class HistoryByIdAPIView(generics.ListAPIView, generics.UpdateAPIView):
    queryset = History.objects.all()
    serializer_class = serializers.HistorySerializer
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.permission_classes = [DoctorOrPacientPermission]
        elif request.method == "PUT":
            self.permission_classes = [AdminOrManagerOrDoctorPermission]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        response = history.get_history(id)
        return response
    def put(self, request, id):
        response = history.put_history(request, id)
        return response
    

class HistoryAPI(generics.CreateAPIView):
    queryset = History.objects.all()
    serializer_class = serializers.HistorySerializer
    permission_classes = [AdminOrManagerOrDoctorPermission]
    def post(self, request):
        response = history.post_history(request)
        return response


class HistoryPacientAPIView(generics.ListAPIView):
    queryset = history.History.objects.all()
    serializer_class = serializers.HistoryAccountByIdSerializer
    permission_classes = [DoctorOrPacientPermission]
    def get(self, request, id):
        response = history.get_history_by_pacient(id)
        return response