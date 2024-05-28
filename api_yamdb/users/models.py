from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import (ROLE_ADMIN, ROLE_ADMIN_NAME, ROLE_MODERATOR,
                                ROLE_MODERATOR_NAME, ROLE_USER, ROLE_USER_NAME)

ROLES = (
    (ROLE_ADMIN, ROLE_ADMIN_NAME),
    (ROLE_MODERATOR, ROLE_MODERATOR_NAME),
    (ROLE_USER, ROLE_USER_NAME),
)


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            "Использовать имя 'me' в качестве username запрещено.",
            params={"value": value},
        )


class User(AbstractUser):
    role = models.CharField(max_length=150, default=ROLE_USER, choices=ROLES)
    bio = models.TextField(blank=True)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            validate_username,
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Letters, digits and @/./+/-/_ only.',
            ),
        ],
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    @property
    def admin_role(self):
        return self.role == ROLE_ADMIN

    @property
    def moderator_role(self):
        return self.role == ROLE_MODERATOR

    @property
    def user_role(self):
        return self.role == ROLE_USER
