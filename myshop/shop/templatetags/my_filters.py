from django import template

register = template.Library()


@register.filter(name='declension_of_products')
def declension_of_products(count):
    suffix = ('товар', 'товара', 'товаров')
    keys = (2, 0, 1, 1, 1, 2)
    mod = count % 100
    if 9 < mod < 20:
        suffix_key = 2
    else:
        suffix_key = keys[min(mod % 10, 5)]
    return suffix[suffix_key]
