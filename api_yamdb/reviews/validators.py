from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_year(value):
    if value > timezone.localtime(timezone.now()).year:
        raise ValidationError(f'Год {value} не должен быть больше текущего')
    if value < 0:
        raise ValidationError(f'Год {value} не должен отрицательным числом')
