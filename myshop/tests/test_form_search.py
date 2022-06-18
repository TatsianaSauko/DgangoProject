from django.test import TestCase

from shop.forms import SearchForm


class SearchFormTest(TestCase):
    """Test cases for form Search"""

    def test_q_placeholder(self):
        form = SearchForm()
        self.assertEqual(form.fields['q'].widget.attrs['placeholder'], 'Поиск')