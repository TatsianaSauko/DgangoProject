from django.test import TestCase
from coupons.models import Coupon
from django.utils import timezone


class CouponModelTest(TestCase):
    """Test cases for model Coupon"""

    @classmethod
    def setUpTestData(cls):
        Coupon.objects.create(code='ABC', valid_from=timezone.now(),
                              valid_to=timezone.now(), discount=50,
                              active=False)

    def test_code_max_length(self):
        obj = Coupon.objects.get(id=1)
        max_length = obj._meta.get_field('code').max_length
        self.assertEqual(max_length, 50)

    def test_code_unique(self):
        obj = Coupon.objects.get(id=1)
        unique = obj._meta.get_field('code').unique
        self.assertTrue(unique)

    def test_code_verbose_name(self):
        obj = Coupon.objects.get(id=1)
        verbose_name = obj._meta.get_field('code').verbose_name
        self.assertEqual(verbose_name, 'Код купона')

    def test_valid_from_verbose_name(self):
        obj = Coupon.objects.get(id=1)
        verbose_name = obj._meta.get_field('valid_from').verbose_name
        self.assertEqual(verbose_name, 'Начало действия купона')

    def test_valid_to_verbose_name(self):
        obj = Coupon.objects.get(id=1)
        verbose_name = obj._meta.get_field('valid_to').verbose_name
        self.assertEqual(verbose_name, 'Окончание действия купона')

    def test_active_verbose_name(self):
        obj = Coupon.objects.get(id=1)
        verbose_name = obj._meta.get_field('active').verbose_name
        self.assertEqual(verbose_name, 'Активность')

    def test_meta_verbose_name(self):
        obj = Coupon.objects.get(id=1)
        verbose_name = obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Скидка')

    def test_meta_verbose_name_plural(self):
        obj = Coupon.objects.get(id=1)
        verbose_name_plural = obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Скидки')

    def test_str(self):
        obj = Coupon.objects.get(id=1)
        self.assertEqual(str(obj), obj.code)
