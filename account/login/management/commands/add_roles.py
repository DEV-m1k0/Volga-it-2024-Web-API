from typing import Any
from django.core.management.base import BaseCommand
from login.models import Role

class Command(BaseCommand):
    help = 'Create main roles'

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            if Role.objects.count() == 0:
                Role.objects.create(role='Admin')
                Role.objects.create(role='Manager')
                Role.objects.create(role='Doctor')
                Role.objects.create(role='User')

                self.stdout.write(self.style.SUCCESS('Роли успешно созданы'))

        except:
            self.stdout.write(self.style.ERROR('Ошибка при создании ролей'))