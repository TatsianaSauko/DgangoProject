from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True, verbose_name='Код купона')
    valid_from = models.DateTimeField(verbose_name='Начало действия купона')
    valid_to = models.DateTimeField(verbose_name='Окончание действия купона')
    discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)], verbose_name='Размер скидки', help_text='В процентах')
    active = models.BooleanField(verbose_name='Активность')

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.code
