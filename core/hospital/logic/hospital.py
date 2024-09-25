from rest_framework.request import Request
from rest_framework.response import Response
from hospital.models import Hospital


def get_all(request: Request):
    hospital = Hospital.objects.all()
    
    if hospital:

        hospitals_count = hospital.count()
        id = hospital[0].pk
        
        return Response({
            "from": id,
            "count": hospitals_count
        })
    
    else:
        return Response({"server": "Больниц еще нет"})