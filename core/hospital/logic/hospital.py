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
    

def get_info_by_id(request: Request, id: int):
    try:
        hospital = Hospital.objects.get(pk=id)

        return Response({
            "name": str(hospital.name),
            "address": str(hospital.address),
            "contactPhone": str(hospital.contactPhone),
            "rooms": get_rooms(hospital=hospital)
        })

    except:
        return Response({
            "server": "Больницы нет"
        })
    

def get_rooms(hospital: Hospital) -> list:
    rooms_list = []

    for room in hospital.rooms.all().values_list('room'):
        rooms_list.append(room[0])

    return rooms_list



