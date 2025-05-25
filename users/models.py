from django.db import models
from django.contrib.auth.models import AbstractUser


class TrackerUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, verbose_name='Город')
    tg_id_chat = models.BigIntegerField(
        verbose_name='Telegram Chat ID',
        null=True,
        blank=True,
        unique=True
    )

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
