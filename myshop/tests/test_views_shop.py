from django.test import TestCase
from shop.models import Category, Product


class ProductListViewTest(TestCase):
    """Test cases for view product_list"""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Main', slug='main')
        for i in range(30):
            Product.objects.create(
                category=Category.objects.get(id=1),
                name='Name' + str(i),
                image='abc.jpg',
                slug='name-' + str(i),
                author='Автор',
                description='Описание книги',
                price=200,
                year=2021,
                pages_num=250
            )

    def test_200(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'shop/product/list.html')
