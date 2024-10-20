


# SECTION - Добавление базовых пользователей
# NOTE Команда для добавления ролей(MacOS): python3 ./manage.py add_users
# NOTE Команда для добавления ролей(Windows): python ./manage.py add_users



from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from api.models import MyUser, Role



class Command(BaseCommand):
    help = 'Create base users'

    def handle(self, *args, **options):
        try:
            if not MyUser.objects.count() and Role.objects.count() == 4:
                admin = MyUser.objects.create(
                    username='admin',
                    email='admin@example.com',
                    is_superuser=True,
                    is_staff=True,
                    lastName="Adminovich",
                    firstName="Admin"
                )
                admin.password = make_password('admin')  # Hash password before saving it in database.
                admin.roles.add(Role.objects.get(role='Admin'))
                admin.save()

                manager = MyUser.objects.create(
                    username='manager',
                    email='manager@example.com',
                    is_superuser=False,
                    is_staff=False,
                    lastName="Managerovich",
                    firstName="Manager"
                    )
                manager.password = make_password('manager')  # Hash password before saving it in database.
                manager.roles.add(Role.objects.get(role='Manager'))
                manager.save()

                doctor = MyUser.objects.create(
                    username='doctor',
                    email='doctor@example.com',
                    is_superuser=False,
                    is_staff=False,
                    lastName="Doctorovich",
                    firstName="Doctor"
                    )
                doctor.password = make_password('doctor')  # Hash password before saving it in database.
                doctor.roles.add(Role.objects.get(role='Doctor'))
                doctor.save()    
            
                user = MyUser.objects.create(
                    username='user',
                    email='user@example.com',
                    is_superuser=False,
                    is_staff=False,
                    lastName="Userovich",
                    firstName="User"
                )
                user.password = make_password('user')  # Hash password before saving it in database.
                user.roles.add(Role.objects.get(role='User'))
                user.save()

                self.stdout.write(self.style.SUCCESS('Базовые пользователи успешно созданы'))

            else:
                self.stdout.write(self.style.WARNING('Пользователи уже существуют или роли не созданы'))


        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при создании базовых пользователей: {str(e)}'))