from django.test import TestCase
from django.core.exceptions import ValidationError
from shop.models import Category, Product


class ProductModelTest(TestCase):
    """Test cases for model Product"""
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Main', slug='main')
        Product.objects.create(
            category=Category.objects.get(id=1),
            name='Name',
            slug='name',
            author='Автор',
            description='Описание книги',
            price=200,
            year=2021,
            pages_num=250
        )

    def test_category_null(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('category').null)

    def test_category_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('category').verbose_name
        self.assertEqual(verbose_name, 'Раздел')

    def test_name_max_length(self):
        obj = Product.objects.get(id=1)
        max_length = obj._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_name_db_index(self):
        obj = Product.objects.get(id=1)
        db_index = obj._meta.get_field('name').db_index
        self.assertTrue(db_index)

    def test_name_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, 'Название')

    def test_slug_max_length(self):
        obj = Product.objects.get(id=1)
        max_length = obj._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)

    def test_slug_db_index(self):
        obj = Product.objects.get(id=1)
        db_index = obj._meta.get_field('slug').db_index
        self.assertTrue(db_index)

    def test_slug_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Псевдоним')

    def test_image_upload_to(self):
        obj = Product.objects.get(id=1)
        self.assertEqual(obj._meta.get_field('image').upload_to, 'products/%Y/%m/%d')

    def test_image_blank(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('image').blank)

    def test_image_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('image').verbose_name
        self.assertEqual(verbose_name, 'Изображение')

    def test_author_max_length(self):
        obj = Product.objects.get(id=1)
        max_length = obj._meta.get_field('author').max_length
        self.assertEqual(max_length, 70)

    def test_author_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('author').verbose_name
        self.assertEqual(verbose_name, 'Автор')

    def test_description_blank(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('description').blank)

    def test_description_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('description').verbose_name
        self.assertEqual(verbose_name, 'Описание')

    def test_price_max_digits(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('price').max_digits, 10)

    def test_price_decimal_places(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('price').decimal_places, 2)

    def test_price_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('price').verbose_name
        self.assertEqual(verbose_name, 'Цена')

    def test_year_validators(self):
        obj = Product.objects.get(id=1)
        obj.year = 1500
        self.assertRaises(ValidationError, obj.full_clean)
        obj.year = 3000
        self.assertRaises(ValidationError, obj.full_clean)

    def test_year_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('year').verbose_name
        self.assertEqual(verbose_name, 'Год издания')

    def test_pages_num_null(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('pages_num').null)

    def test_pages_num_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('pages_num').verbose_name
        self.assertEqual(verbose_name, 'Страниц')

    def test_pages_num_blank(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('pages_num').blank)

    def test_available_default(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('available').default)

    def test_available_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('available').verbose_name
        self.assertEqual(verbose_name, 'Доступность')

    def test_created_auto_now_add(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('created').auto_now_add)

    def test_created_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('created').verbose_name
        self.assertEqual(verbose_name, 'Дата добавления')

    def test_updated_auto_auto_now(self):
        obj = Product.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('updated').auto_now)

    def test_updated_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.get_field('updated').verbose_name
        self.assertEqual(verbose_name, 'Дата изменения')

    def test_meta_ordering(self):
        obj = Product.objects.get(id=1)
        ordering = obj._meta.ordering
        self.assertEqual(ordering, ('name',))

    def test_meta_index_together(self):
        obj = Product.objects.get(id=1)
        index_together = obj._meta.index_together
        self.assertEqual(index_together, (('id', 'slug'),))

    def test_meta_verbose_name(self):
        obj = Product.objects.get(id=1)
        verbose_name = obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Товар')

    def test_meta_verbose_name_plural(self):
        obj = Product.objects.get(id=1)
        verbose_name_plural = obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Товары')

    def test_str(self):
        obj = Product.objects.get(id=1)
        self.assertEqual(str(obj), obj.name)

    def test_get_absolute_url(self):
        obj = Product.objects.get(id=1)
        self.assertEqual(obj.get_absolute_url(), '/' + str(obj.id) + '/' + obj.slug + '/')
