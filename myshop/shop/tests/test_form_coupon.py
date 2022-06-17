from django.test import TestCase

from coupons.forms import CouponApplyForm


class CouponFormTest(TestCase):
    """Test cases for form Coupon"""

    def test_code_label(self):
        form = CouponApplyForm()
        self.assertEqual(form.fields['code'].label, 'Введите номер купона со скидкой')