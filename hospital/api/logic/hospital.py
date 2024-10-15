from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from api.models import Hospital, Room


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
        return Response({"server": "Больниц еще нет"}, status=status.HTTP_404_NOT_FOUND)
    

def get_info_by_id(request: Request, id: int):
    try:
        hospital = Hospital.objects.get(pk=id)

        return Response({
            "name": str(hospital.name),
            "address": str(hospital.address),
            "contactPhone": str(hospital.contactPhone),
            "rooms": get_rooms(hospital=hospital)
        }, status=status.HTTP_200_OK)

    except:
        return Response({
            "server": "Больницы нет"
        }, status=status.HTTP_404_NOT_FOUND)
    

def get_rooms(hospital: Hospital) -> list:
    rooms_list = []

    for room in hospital.rooms.all().values_list('room'):
        rooms_list.append(room[0])

    return rooms_list


def hospital_create(request: Request):
    response = {}

    if isinstance(request.data, dict):
        hospital = Hospital
        response.update(add_hospital(request.data, hospital=hospital))

    elif isinstance(request.data, list):

        for data in request.data:
            hospital = Hospital
            response.update(add_hospital(data, hospital))

    else:
        return Response({
            "SERVER_ERROR": "Не удалось добавить больницу. Пожалуйства, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(response)


def add_hospital(data: dict, hospital: Hospital):

    response = {}

    try:
        hospital = hospital.objects.create(
            name=data["name"],
            address=data["address"],
            contactPhone=data['contactPhone'],
        )

        add_room(request_rooms=data["rooms"], hospital=hospital)

        response[f"{hospital.name}"] = "Успешно добавлена"

        return response


    except:
        response["SERVER_ERROR"] = "Не удалось добавить больницу. Пожалуйства, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        return response


def add_room(request_rooms: list, hospital: Hospital):

    has, has_not = check_rooms(rooms=request_rooms)

    rooms = []

    for new_room in has_not:
        room = Room.objects.create(
            room=str(new_room)
        )
        room.id_hospital.add(hospital)
        room.save()
        rooms.append(room)

    for room_has in has:
        rooms.append(Room.objects.get(
            room=room_has
        ))

    hospital.rooms.set(rooms)


def check_rooms(rooms: list):
    all_rooms = Room.objects.all()

    rooms_list = []

    rooms_has = []
    rooms_has_not = []

    for obj_room in all_rooms:
        rooms_list.append(obj_room.room)

    for request_room in rooms:
        if request_room in rooms_list:
            rooms_has.append(request_room)

        else:
            rooms_has_not.append(request_room)

    return rooms_has, rooms_has_not


def update_hospital_by_id(request: Request, id: int):

    response = {}
    hospital = Hospital.objects.get(pk=id)

    try:
        hospital.name = request.data['name']
        hospital.address = request.data['address']
        hospital.contactPhone = request.data['contactPhone']

        hospital.save()

        response[f"{hospital.name}"] = "Была успешно обновлена"

        add_room(request_rooms=request.data['rooms'], hospital=hospital)

        return Response(response)

    except:
        return Response({
            f"ERROR_{hospital.name}": "Больница не была обновлена. Пожалуйства, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        }, status=status.HTTP_400_BAD_REQUEST)
    

def delete_hospital_by_id(request: Request, id: int):

    response = {}
    hospital = Hospital.objects.get(pk=id)
    hospital_name = hospital.name

    try:
        hospital.delete()
        response[f"{hospital_name}"] = "Больница была успешно удалена"

        return Response(response)

    except:
        return Response({
            f"ERROR_{hospital.name}": "Больница не была удалена. Пожалуйства, проверьте ваш json и убедитесь, что в нем нет ошибок и наименования полей верны!"
        })