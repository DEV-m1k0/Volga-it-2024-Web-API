from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .logic import hospital

# Create your views here.


class HospitalsAPIView(APIView):
    def get(self, request: Request, id: int = False):

        if id:
            response = hospital.get_info_by_id(request=request, id=id)
            return response
        
        else:
            response = hospital.get_all(request=request)
            return response