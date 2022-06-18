from django.test import TestCase
from orders.models import Order, OrderItem
from shop.models import Category, Product


class OrderItemModelTest(TestCase):
    """Test cases for model OrderItem"""

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

    def test_order_verbose_name(self):
        obj = OrderItem.objects.get(id=1)
        verbose_name = obj._meta.get_field('order').verbose_name
        self.assertEqual(verbose_name, 'Заказ')

    def test_product_verbose_name(self):
        obj = OrderItem.objects.get(id=1)
        verbose_name = obj._meta.get_field('product').verbose_name
        self.assertEqual(verbose_name, 'Товар')

    def test_price_max_digits(self):
        obj = OrderItem.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('price').max_digits, 10)

    def test_price_decimal_places(self):
        obj = OrderItem.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('price').decimal_places, 2)

    def test_price_verbose_name(self):
        obj = OrderItem.objects.get(id=1)
        verbose_name = obj._meta.get_field('price').verbose_name
        self.assertEqual(verbose_name, 'Цена')

    def test_quantity_default(self):
        obj = OrderItem.objects.get(id=1)
        default = obj._meta.get_field('quantity').default
        self.assertEqual(default, 1)

    def test_quantity_verbose_name(self):
        obj = OrderItem.objects.get(id=1)
        verbose_name = obj._meta.get_field('quantity').verbose_name
        self.assertEqual(verbose_name, 'Количество')

    def test_meta_verbose_name(self):
        obj = OrderItem.objects.get(id=1)
        verbose_name = obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Строка заказа')

    def test_meta_verbose_name_plural(self):
        obj = OrderItem.objects.get(id=1)
        verbose_name_plural = obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Строки заказов')

    def test_str(self):
        obj = OrderItem.objects.get(id=1)
        self.assertEqual(str(obj), '1')

    def test_get_cost(self):
        obj = OrderItem.objects.get(id=1)
        get_cost = obj.get_cost()
        self.assertEqual(get_cost, 1000)
