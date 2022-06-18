from django.core.exceptions import ValidationError
from django.test import TestCase
from orders.models import Order, OrderItem
from shop.models import Category, Product


class OrderModelTest(TestCase):
    """Test cases for model Order"""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Main', slug='main')
        Product.objects.create(
            category=Category.objects.get(id=1),
            name='Name',
            slug='name',
            author='Автор',
            description='Описание книги',
            price=200,
            year=2021,
            pages_num=250
        )
        Order.objects.create(
            need_delivery=False,
            first_name='Имя',
            last_name='Фамилия',
            phone='3235235',
            email='abc@example.com',
            address=''
        )
        OrderItem.objects.create(
            order=Order.objects.get(id=1),
            product=Product.objects.get(id=1),
            price=Product.objects.get(id=1).price,
            quantity=5
        )

    def test_first_name_max_length(self):
        obj = Order.objects.get(id=1)
        max_length = obj._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 50)

    def test_first_name_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('first_name').verbose_name
        self.assertEqual(verbose_name, 'Имя')

    def test_last_name_max_length(self):
        obj = Order.objects.get(id=1)
        max_length = obj._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 50)

    def test_last_name_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('last_name').verbose_name
        self.assertEqual(verbose_name, 'Фамилия')

    def test_phone_max_length(self):
        obj = Order.objects.get(id=1)
        max_length = obj._meta.get_field('phone').max_length
        self.assertEqual(max_length, 70)

    def test_phone_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('phone').verbose_name
        self.assertEqual(verbose_name, 'Телефон')

    def test_address_max_length(self):
        obj = Order.objects.get(id=1)
        max_length = obj._meta.get_field('address').max_length
        self.assertEqual(max_length, 250)

    def test_address_blank(self):
        obj = Order.objects.get(id=1)
        blank = obj._meta.get_field('address').blank
        self.assertTrue(blank)

    def test_address_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('address').verbose_name
        self.assertEqual(verbose_name, 'Адрес')

    def test_created_auto_now_add(self):
        obj = Order.objects.get(id=1)
        auto_now_add = obj._meta.get_field('created').auto_now_add
        self.assertTrue(auto_now_add)

    def test_created_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('created').verbose_name
        self.assertEqual(verbose_name, 'Дата заказа')

    def test_updated_auto_now(self):
        obj = Order.objects.get(id=1)
        auto_now = obj._meta.get_field('updated').auto_now
        self.assertTrue(auto_now)

    def test_updated_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('updated').verbose_name
        self.assertEqual(verbose_name, 'Дата изменения')

    def test_need_delivery_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('need_delivery').verbose_name
        self.assertEqual(verbose_name, 'Доставка')

    def test_notice_blank(self):
        obj = Order.objects.get(id=1)
        blank = obj._meta.get_field('notice').blank
        self.assertTrue(blank)

    def test_notice_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('notice').verbose_name
        self.assertEqual(verbose_name, 'Примечание к заказу')

    def test_paid_default(self):
        obj = Order.objects.get(id=1)
        default = obj._meta.get_field('paid').default
        self.assertFalse(default)

    def test_paid_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('paid').verbose_name
        self.assertEqual(verbose_name, 'Оплата')

    def test_coupon_null(self):
        obj = Order.objects.get(id=1)
        null = obj._meta.get_field('coupon').null
        self.assertTrue(null)

    def test_coupon_blank(self):
        obj = Order.objects.get(id=1)
        blank = obj._meta.get_field('coupon').blank
        self.assertTrue(blank)

    def test_coupon_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('coupon').verbose_name
        self.assertEqual(verbose_name, 'Купон')

    def test_discount_default(self):
        obj = Order.objects.get(id=1)
        default = obj._meta.get_field('discount').default
        self.assertEqual(default, 0)

    def test_discount_validators(self):
        obj = Order.objects.get(id=1)
        obj.discount = -10
        self.assertRaises(ValidationError, obj.full_clean)
        obj.discount = 110
        self.assertRaises(ValidationError, obj.full_clean)

    def test_discount_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('discount').verbose_name
        self.assertEqual(verbose_name, 'Скидка')

    def test_status_choices(self):
        STATUSES = [
            ('NEW', 'Новый заказ'),
            ('APR', 'Подтверждён'),
            ('PAY', 'Оплачен'),
            ('CNL', 'Отменён')
        ]
        obj = Order.objects.get(id=1)
        self.assertEqual(obj._meta.get_field('status').choices, STATUSES)

    def test_status_max_length(self):
        obj = Order.objects.get(id=1)
        max_length = obj._meta.get_field('status').max_length
        self.assertEqual(max_length, 3)

    def test_status_default(self):
        obj = Order.objects.get(id=1)
        default = obj._meta.get_field('status').default
        self.assertEqual(default, 'NEW')

    def test_status_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.get_field('status').verbose_name
        self.assertEqual(verbose_name, 'Статус')

    def test_meta_ordering(self):
        obj = Order.objects.get(id=1)
        ordering = obj._meta.ordering
        self.assertEqual(ordering, ('-created',))

    def test_meta_verbose_name(self):
        obj = Order.objects.get(id=1)
        verbose_name = obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Заказ')

    def test_meta_verbose_name_plural(self):
        obj = Order.objects.get(id=1)
        verbose_name_plural = obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Заказы')

    def test_meta_permissions(self):
        obj = Order.objects.get(id=1)
        permissions = obj._meta.permissions
        self.assertEqual(permissions, (('can_set_status', 'Возможность настройки статуса'), ))

    def test_str(self):
        obj = Order.objects.get(id=1)
        self.assertEqual(str(obj), 'Order 1')

    def test_display_products(self):
        obj = Order.objects.get(id=1)
        display_products = obj.display_products()
        self.assertEqual(display_products, 'Name: 5 шт.; ')

    def test_get_total_cost(self):
        obj = Order.objects.get(id=1)
        get_total_cost = obj.get_total_cost()
        self.assertEqual(get_total_cost, 1000)

    def test_display_products_short_description(self):
        obj = Order.objects.get(id=1)
        short_description = obj.display_products.short_description
        self.assertEqual(short_description, 'Состав заказа')

    def test_get_total_cost_short_description(self):
        obj = Order.objects.get(id=1)
        short_description = obj.get_total_cost.short_description
        self.assertEqual(short_description, 'Сумма')
