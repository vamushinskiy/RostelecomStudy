from .models import ViewCount

# Получаем IP адрес
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Проверяем просмотры на уникальность
class ViewCountMixin:
    def get_object(self):
        # Получаем объект из родительского класса
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        # Если такой счётчик уже сущестует, то выполняется get - получение
        # если счётчика нет, то выполняется - Create создание
        ViewCount.objects.get_or_create(article=obj, ip_address=ip_address)
        return obj