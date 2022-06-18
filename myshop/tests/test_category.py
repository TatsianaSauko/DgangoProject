from django.test import TestCase
from shop.models import Category


class CategoryModelTest(TestCase):
    """Test cases for model Category"""
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Main', slug='main')

    def test_name_max_length(self):
        obj = Category.objects.get(id=1)
        max_length = obj._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_name_db_index(self):
        obj = Category.objects.get(id=1)
        db_index = obj._meta.get_field('name').db_index
        self.assertTrue(db_index)

    def test_name_help_text(self):
        obj = Category.objects.get(id=1)
        help_text = obj._meta.get_field('name').help_text
        self.assertEqual(help_text, 'Тут надо ввести название раздела')

    def test_name_unique(self):
        obj = Category.objects.get(id=1)
        unique = obj._meta.get_field('name').unique
        self.assertTrue(unique)

    def test_name_verbose_name(self):
        obj = Category.objects.get(id=1)
        verbose_name = obj._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, 'Название раздела')

    def test_slug_max_length(self):
        obj = Category.objects.get(id=1)
        max_length = obj._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)

    def test_slug_unique(self):
        obj = Category.objects.get(id=1)
        unique = obj._meta.get_field('slug').unique
        self.assertTrue(unique)

    def test_slug_verbose_name(self):
        obj = Category.objects.get(id=1)
        verbose_name = obj._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Псевдоним')

    def test_meta_ordering(self):
        obj = Category.objects.get(id=1)
        ordering = obj._meta.ordering
        self.assertEqual(ordering, ('name',))

    def test_meta_verbose_name(self):
        obj = Category.objects.get(id=1)
        verbose_name = obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Раздел')

    def test_meta_verbose_name_plural(self):
        obj = Category.objects.get(id=1)
        verbose_name_plural = obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Разделы')

    def test_get_absolute_url(self):
        obj = Category.objects.get(id=1)
        self.assertEqual(obj.get_absolute_url(), '/' + obj.slug + '/')

    def test_str(self):
        obj = Category.objects.get(id=1)
        self.assertEqual(str(obj), obj.name)
