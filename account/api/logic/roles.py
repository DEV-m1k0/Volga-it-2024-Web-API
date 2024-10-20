


# SECTION - Бизнес логика для добавления ролей из микросервиса Account



from typing import Any
from api.models import CHOICES_ROLE_FOR_MYUSER, MyUser, Role



def add_role(user: MyUser, validate_data: dict[str, Any]):

    check_role = _role_is_exist(validate_data['roles'])

    response = {}

    try:
        if check_role:
            roles = list(Role.objects.filter(role__in=validate_data['roles']))
            user.roles.set(roles)

        else:
            response[f"{user}"] = "Роли не были добавлены. Убедитесь в корректности введенных ролей"

    except:
        response["server"] = "ошибка при назначении ролей"

    return response


def _role_is_exist(roles: list[str]) -> bool:
    try:
        roles_count = len(roles)
        counter = 0

        for role in roles:
            for my_role in CHOICES_ROLE_FOR_MYUSER:
                if role in my_role:
                    counter += 1
                    break

        if (counter == roles_count): return True
        
        else: return False

    except:
        return False