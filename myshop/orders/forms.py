from django import forms
from django.core.exceptions import ValidationError

from .models import Order


class OrderCreateForm(forms.ModelForm):
    DELIVERY_CHOICES = (
        (0, 'Выберите, пожалуйста'),
        (1, 'Доставка'),
        (2, 'Самовывоз'),
    )
    delivery = forms.TypedChoiceField(label='Доставка',
                                      choices=DELIVERY_CHOICES, coerce=int)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'need_delivery', 'notice']

        labels = {
            'address': 'Полный адрес (Страна, город, индекс, улица, дом, квартира)'}
        widgets = {
            'address': forms.Textarea(
                attrs={'rows': 6, 'cols': 80,
                       'placeholder': 'При самовывозе можно оставить это поле пустым'}
            ),
            'notice': forms.Textarea(
                attrs={'rows': 6, 'cols': 80}
            )
        }

    def clean_delivery(self):
        data = self.cleaned_data['delivery']
        if data == 0:
            raise ValidationError('Необходимо выбрать способ доставки')
        return data

    def clean(self):
        try:
            delivery = self.cleaned_data['delivery']
            address = self.cleaned_data['address']
            if delivery == 1 and address == '':
                raise ValidationError('Укажите адрес доставки')
            return self.cleaned_data
        except KeyError:
            pass