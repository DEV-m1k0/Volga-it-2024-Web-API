from django.apps import AppConfig


class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

    # def ready(self):
    #     from django.core.management import call_command
    #     call_command("add_users.py")