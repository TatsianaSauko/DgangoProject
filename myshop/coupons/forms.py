from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(label='Введите номер купона со скидкой')
