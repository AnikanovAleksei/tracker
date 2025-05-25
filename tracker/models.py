from django.core.exceptions import ValidationError
from django.db import models
from users.models import TrackerUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Tracker(models.Model):
    DAILY = 1
    WEEKLY = 7
    MONTHLY = 30

    PERIODICITY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно'),
    ]

    user = models.ForeignKey(TrackerUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    place = models.TextField(verbose_name='Место', null=True, blank=True,)
    data = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    action = models.CharField(max_length=250, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Связанная привычка', related_name='main_habit')
    periodicity = models.PositiveSmallIntegerField(choices=PERIODICITY_CHOICES, default=DAILY,
                                                   verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)],
                                           verbose_name='Время на выполнение (в секундах)', null=True, blank=True,)
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    next_reminder = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'Я - {self.user} буду {self.action} в {self.data} в {self.place}'

    def clean(self):
        if self.is_pleasant:
            if self.reward:
                raise ValidationError('У приятной привычки не может быть вознаграждения')

            if self.related_habit:
                raise ValidationError(
                    {'related_habit': 'У приятной привычки не может быть связанной привычки'}
                )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                {'related_habit': 'В связанные привычки могут попадать только привычки с признаком приятной привычки'}
            )

        if self.reward and self.related_habit:
            raise ValidationError(
                'Нельзя одновременно указывать связанную привычку и вознаграждение. Выберите что-то одно.'
            )

        if self.periodicity < 7:
            raise ValidationError(
                {'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
