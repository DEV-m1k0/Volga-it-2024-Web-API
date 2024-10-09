import pytest
from api.models import TimeTable, MyUser, Room, Hospital, Role
import requests as rq
from django.contrib.auth.hashers import make_password, check_password


@pytest.fixture
def authenticate(request):

    admin = MyUser.objects.create_user(username='test_admin', password='admin')
    role = Role.objects.create(role='Admin')
    admin.roles.add(role)
    admin.save()

    link = 'http://127.0.0.1:8000/api/Authentication/SignIn/'

    tokens = rq.post(link, json={'username': admin.username, 'password': admin.password}).json()
    print(f"\nToken: {tokens}")

    def token_delete():
        admin.delete()
        role.delete()
    request.addfinalizer(token_delete)
    # return token


@pytest.mark.django_db
def test_get(authenticate):
    link = 'http://127.0.0.1:8001/api/Timetable/Hospital/1/'
    response = rq.get(link)
    print(response.json())