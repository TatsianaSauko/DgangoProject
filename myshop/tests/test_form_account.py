from django.contrib.auth.models import User
from django.test import TestCase

from account.forms import UserRegistrationForm


class AccountFormTest(TestCase):
    """Test cases for form Account"""

    def test_password_label(self):
        form = UserRegistrationForm()
        self.assertEqual(form.fields['password'].label, 'Пароль')

    def test_password2_label(self):
        form = UserRegistrationForm()
        self.assertEqual(form.fields['password2'].label, 'Повторите пароль')

    def test_meta_model(self):
        form = UserRegistrationForm()
        self.assertEqual(form._meta.model, User)

    def test_meta_fields(self):
        form = UserRegistrationForm()
        self.assertEqual(form._meta.fields,
                         ('username', 'first_name', 'email'))
