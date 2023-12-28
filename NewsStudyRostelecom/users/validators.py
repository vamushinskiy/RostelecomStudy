from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

# Проверка почтовых доменов на допустимость
def acceptable_email(email):
    acceptable_domains = ['@mail.ru',
                       '@mil.ru',
                       '@yandex.ru']
    if not any(domain in email for domain in acceptable_domains):
        # Сообщение об ошибке обязательно на английском языке,  с кириллицей возникает ошибка.
        raise ValidationError(
            _("%(email) has not allowed domain"),params={'email':email}
        )