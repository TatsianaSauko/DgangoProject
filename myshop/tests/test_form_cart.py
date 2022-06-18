from unittest import TestCase
from cart.forms import CartAddProductForm


class CartFormTest(TestCase):
    """Test cases for form Cart"""

    def test_quantity_choices(self):
        PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
        form = CartAddProductForm()
        self.assertEqual(form.fields['quantity'].choices, PRODUCT_QUANTITY_CHOICES)

    def test_quantity_coerce(self):
        form = CartAddProductForm()
        self.assertEqual(form.fields['quantity'].coerce, int)

    def test_quantity_label(self):
        form = CartAddProductForm()
        self.assertEqual(form.fields['quantity'].label, 'Количество')

    def test_update_required(self):
        form = CartAddProductForm()
        self.assertFalse(form.fields['update'].required)

    def test_update_initial(self):
        form = CartAddProductForm()
        self.assertFalse(form.fields['update'].initial)

    def test_update_widget(self):
        form = CartAddProductForm()
        self.assertTrue(form.fields['update'].widget)
