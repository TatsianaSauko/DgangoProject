from django.db import models

from coupons.models import Coupon
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.CharField(max_length=70, verbose_name='Телефон')
    email = models.EmailField()
    address = models.CharField(max_length=250, blank=True, verbose_name='Адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    need_delivery = models.BooleanField(verbose_name='Доставка')
    notice = models.TextField(blank=True, verbose_name='Примечание к заказу')
    paid = models.BooleanField(default=False, verbose_name='Оплата')
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL, verbose_name="Купон")
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)], verbose_name="Скидка")
    STATUSES = [
        ('NEW', 'Новый заказ'),
        ('APR', 'Подтверждён'),
        ('PAY', 'Оплачен'),
        ('CNL', 'Отменён')
    ]

    status = models.CharField(choices=STATUSES, max_length=3, default='NEW',
                              verbose_name='Статус')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        permissions = (('can_set_status', 'Возможность настройки статуса'),)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def display_products(self):
        display = ''
        for order_item in self.items.all():
            display += '{0}: {1} шт.; '.format(order_item.product.name, order_item.quantity)
        return display

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return round(total_cost - total_cost * (self.discount / Decimal('100')), 2)

    display_products.short_description = 'Состав заказа'
    get_total_cost.short_description = 'Сумма'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказов'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity