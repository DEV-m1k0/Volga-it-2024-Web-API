from rest_framework.views import APIView
from rest_framework.request import Request
from .logic import hospital

# Create your views here.


class HospitalsAPIView(APIView):
    def get(self, request: Request):
        response = hospital.get_all(request=request)

        return response