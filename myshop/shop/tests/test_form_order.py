from unittest import TestCase

from orders.forms import OrderCreateForm
from orders.models import Order


class OrderFormTest(TestCase):
    """Test cases for form Order"""

    def test_delivery_choices(self):
        DELIVERY_CHOICES = [
            (0, 'Выберите, пожалуйста'),
            (1, 'Доставка'),
            (2, 'Самовывоз'),
        ]
        form = OrderCreateForm()
        self.assertEqual(form.fields['delivery'].choices, DELIVERY_CHOICES)

    def test_delivery_label(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['delivery'].label, 'Доставка')

    def test_delivery_coerce(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['delivery'].coerce, int)

    def test_meta_model(self):
        form = OrderCreateForm()
        self.assertEqual(form._meta.model, Order)

    def test_meta_fields(self):
        form = OrderCreateForm()
        self.assertEqual(form._meta.fields,
                         ['first_name', 'last_name', 'phone', 'email',
                          'address', 'need_delivery', 'notice'])

    def test_meta_labels(self):
        form = OrderCreateForm()
        self.assertEqual(form._meta.labels, {
            'address': 'Полный адрес (Страна, город, индекс, улица, дом, квартира)'})

    def test_widgets_address_rows(self):
        form = OrderCreateForm()
        self.assertEqual(form._meta.widgets['address'].attrs['rows'], 6)

    def test_widgets_address_cols(self):
        form = OrderCreateForm()
        self.assertEqual(form._meta.widgets['address'].attrs['cols'], 80)

    def test_widgets_address_placeholder(self):
        form = OrderCreateForm()
        self.assertEqual(form._meta.widgets['address'].attrs['placeholder'],
                         'При самовывозе можно оставить это поле пустым')

    def test_widgets_notice_rows(self):
        form = OrderCreateForm()
        self.assertEqual(form._meta.widgets['notice'].attrs['rows'], 6)

    def test_widgets_notice_cols(self):
        form = OrderCreateForm()
        self.assertEqual(form._meta.widgets['notice'].attrs['cols'], 80)

    def test_valid_delivery_0(self):
        data = {'first_name': 'Имя', 'last_name': 'Фамилия',
                'email': 'abc@example.com', 'phone': '3123455',
                'address': 'Адрес', 'delivery': 0}
        form = OrderCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_delivery_1_without_address(self):
        data = {'first_name': 'Имя', 'last_name': 'Фамилия',
                'email': 'abc@example.com', 'phone': '3123455', 'address': '',
                'delivery': 1}
        form = OrderCreateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_delivery_1_with_address(self):
        data = {'first_name': 'Имя', 'last_name': 'Фамилия',
                'email': 'abc@example.com', 'phone': '3123455',
                'address': 'Адрес', 'delivery': 1}
        form = OrderCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_delivery_2(self):
        data = {'first_name': 'Имя', 'last_name': 'Фамилия',
                'email': 'abc@example.com', 'phone': '3123455', 'address': '',
                'delivery': 2}
        form = OrderCreateForm(data=data)
        self.assertTrue(form.is_valid())
