from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .logic.hospital import get_all, get_rooms, get_info_by_id
from .models import Hospital

# Create your views here.


class HospitalsAPIView(APIView):
    def get(self, request: Request, id: int = False):

        if id:
            response = get_info_by_id(request=request, id=id)
            return response
        
        else:
            response = get_all(request=request)
            return response
        

class RoomsByIdAPIVIew(APIView):
    def get(self, request: Request, id: int):

        hospital = Hospital.objects.get(pk=id)
        rooms = get_rooms(hospital=hospital)

        return Response({
            "rooms": rooms
        })