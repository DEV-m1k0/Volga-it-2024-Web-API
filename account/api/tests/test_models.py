import pytest
from api.models import MyUser, Role
from django.contrib.auth import hashers


@pytest.fixture
def role(request):
    role = Role.objects.create(role="Admin")
    print(f"\nRole: {role.role} created")
    def role_delete():
        print(f"\nRole: {role.role} deleted")
        role.delete()
    request.addfinalizer(role_delete)
    return role


@pytest.mark.django_db
def test_create_role(role):
    assert role.role == "Admin"



@pytest.fixture
def user(request):
    user = MyUser.objects.create_user(username="test", password="test", 
                                      email="test@example.com")
    print(f"\nUser: {user.username} created")
    def user_delete():
        print(f"\nUser: {user.username} deleted")
        user.delete()
    request.addfinalizer(user_delete)
    return user


@pytest.mark.django_db
def test_create_user(user):
    assert user.username == "test"
    assert user.email == "test@example.com"
    assert user.password != "test"
    assert True == hashers.check_password("test", user.password)

