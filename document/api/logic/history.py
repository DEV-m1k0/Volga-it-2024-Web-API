


# SECTION - Бизнес логика для работы с историями пользователей для микросервиса Document



from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from api.models import History, MyUser, Hospital, Room
from . import date, validate_data


def put_history(request: Request, id: int):
    try:
        response = {}
        history: History = History.objects.get(pk=id)
        data = request.data
        response_parsed_date = date.parse_one_date(request.data['date'])
        if not response_parsed_date[0]:
            raise Exception('Неправильный формат даты')

        answer_validate_user = validate_data.validate_pacient(request.data['pacientId'], response_parsed_date[1])
        if not answer_validate_user:
            raise Exception('Пациент с таким ID не найден или у данного пациента не было записи на данное время')

        answer_check_hospital = validate_data.check_hospital(request.data['hospitalId'])
        if not answer_check_hospital:
            raise Exception('Больница с таким ID не найдена')
        
        answe_check_doctor = validate_data.check_doctor(request.data['doctorId'])
        if not answe_check_doctor:
            raise Exception('Доктор с таким ID не найден')

        answer_check_room = validate_data.check_room(request.data['room'], request.data['hospitalId'])
        if not answer_check_room:
            raise Exception("Кабинет в данной больнице не найден или такого кабинета еще не существует")

        history.pacientId=MyUser.objects.get(pk=data['pacientId'])
        history.hospitalId=Hospital.objects.get(pk=data['hospitalId'])
        history.doctorId=MyUser.objects.get(pk=data['doctorId'])
        history.room=Room.objects.get(room=data['room'])
        history.date=request.data['date']
        history.data=data['data']
        history.save()

        response = {
            "id": history.pk,
            "pacientId": history.pacientId.pk,
            "hospitalId": history.hospitalId.pk,
            "doctorId": history.doctorId.pk,
            "room": history.room.room,
            "date": history.date,
            "data": history.data,
        }

        return Response({"Измененная запись": response}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"ERROR": f"{e}"}, status=status.HTTP_404_NOT_FOUND)


def get_history_by_pacient(id):
    try:
        response = {}
        pacient = MyUser.objects.get(pk=id)
        answer_pacient = validate_data.check_pacient(id)
        if not answer_pacient:
            return Response({f"Пользователь: {pacient.get_full_name()}": "Данный пользователь не является пациентом, так как у него нет активных записей на прием!"}, status=status.HTTP_404_NOT_FOUND)
        
        historys = History.objects.filter(pacientId=pacient).order_by('-date')
        for i in range(len(historys)):
            response[f'{i+1}'] = {
                "id": historys[i].pk,
                "pacientId": historys[i].pacientId.pk,
                "hospitalId": historys[i].hospitalId.pk,
                "doctorId": historys[i].doctorId.pk,
                "room": historys[i].room.room,
                "date": historys[i].date,
                "data": historys[i].data,
            }

        return Response({f"История: {pacient.get_full_name()}": response}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"error": "История пациента с таким ID не найдена"}, status=status.HTTP_404_NOT_FOUND)


def get_history(id):
    try:
        history = History.objects.get(pk=id)

        return Response({
            "date": history.date,
            "pacientId": history.pacientId.pk,
            "hospitalId": history.hospitalId.pk,
            "doctorId": history.doctorId.pk,
            "room": history.room.room,
            "data": history.data,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"error": "История с таким ID не найдена"}, status=status.HTTP_404_NOT_FOUND)


def post_history(request: Request):
    try:
        response_parsed_date = date.parse_one_date(request.data['date'])
        if not response_parsed_date[0]:
            raise Exception('Неправильный формат даты')
        
        answer_validate_user = validate_data.validate_pacient(request.data['pacientId'], response_parsed_date[1])
        if not answer_validate_user:
            raise Exception('Пациент с таким ID не найден или у данного доктора нет на данное время расписания')

        answer_check_hospital = validate_data.check_hospital(request.data['hospitalId'])
        if not answer_check_hospital:
            raise Exception('Больница с таким ID не найдена')

        answer_check_room = validate_data.check_room(request.data['room'], request.data['hospitalId'])
        if not answer_check_room:
            raise Exception("Кабинет в данной больнице не найден или такого кабинета еще не существует")

        pacient = MyUser.objects.get(pk=request.data['pacientId'])
        hospital = Hospital.objects.get(pk=request.data['hospitalId'])
        doctor = MyUser.objects.get(pk=request.data['doctorId'])
        room = Room.objects.get(room=request.data['room'])

        history = History.objects.create(
            date=request.data.get('date'),
            pacientId=pacient,
            hospitalId=hospital,
            doctorId=doctor,
            room=room,
            data=request.data.get('data')
        )
        
        pacient.history.add(history)
        pacient.save()

        return Response({"message": "История успешно создана"}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        print(e)
        return Response({"ERROR": str(e)}, status=status.HTTP_400_BAD_REQUEST)