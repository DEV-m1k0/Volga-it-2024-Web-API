from django.utils import timezone
from api.models import TimeTable
from datetime import datetime, timedelta
from api.models import Room

def time_to_iso8601_from_db(dates: list[TimeTable]) -> list[str]:
    correct_date = []

    for date in dates:
        date_from = str(timezone.datetime.isoformat(date.date_from)).split('+')[0]+'Z'
        date_to = str(timezone.datetime.isoformat(date.date_to)).split('+')[0]+'Z'
        correct_date.append([date_from, date_to])

    return correct_date


def time_to_iso8601(date: datetime):
    return str(timezone.datetime.isoformat(date)).split('+')[0]+'Z'


def parse_date(request_from: str, request_to: str):
    # Проверка формата дат
    try:
        from_dt = datetime.strptime(request_from, '%Y-%m-%dT%H:%M:%SZ')
        to_dt = datetime.strptime(request_to, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return False
    
    # Проверка времени от и до
    if not ((from_dt.minute % 30 == 0) and (from_dt.second == 0)):
        return False
    if not ((to_dt.minute % 30 == 0) and (to_dt.second == 0)):
        return False
    
    # Проверка интервала между датами
    if from_dt > to_dt:
        return False
    
    diff = to_dt - from_dt
    hours_diff = diff.total_seconds() / 60 ** 2

    if hours_diff <= 12:
        return True, from_dt, to_dt
    
    return False


def check_date_for_room_update(room: Room):
    try:
        tt_room: TimeTable = room.timetable

        if tt_room.appointments.all().exists():
            return False
            
        return True
    except Exception as e:
        print(e)
        return True

def check_date(time_from: datetime, time_to: datetime):
    time_table_all = TimeTable.objects.all()

    for time_table in time_table_all:
        date_from_by_db = datetime.fromisoformat(str(time_table.date_from)).astimezone(timezone.utc)
        date_to_by_db = datetime.fromisoformat(str(time_table.date_to)).astimezone(timezone.utc)
        time_from_by_request = time_from.astimezone(timezone.utc)
        time_to_by_request = time_to.astimezone(timezone.utc)
        
        if (date_from_by_db <= time_from_by_request <= date_to_by_db) or (date_from_by_db <= time_to_by_request <= date_to_by_db):
            return False
        
    return True


def get_appointments(datetime_from: datetime, datetime_to: datetime) -> list[datetime]:
    list_appointments = []
    time_appointment = datetime_from

    while time_appointment <= datetime_to:
        list_appointments.append(time_appointment)
        time_appointment += timedelta(minutes=30)

    return list_appointments