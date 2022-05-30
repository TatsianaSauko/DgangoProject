import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True,
                            help_text='Тут надо ввести название раздела',
                            unique=True,
                            verbose_name='Название раздела')
    slug = models.SlugField(max_length=200,
                            unique=True, verbose_name='Псевдоним')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 null=True, verbose_name='Раздел')
    name = models.CharField(max_length=200, db_index=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True,
                            verbose_name='Псевдоним')
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True, verbose_name='Изображение')
    author = models.CharField(max_length=70, verbose_name='Автор')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена')
    year = models.IntegerField(
        validators=[MinValueValidator(1900),
                    MaxValueValidator(datetime.date.today().year)],
        verbose_name='Год издания'
    )
    pages_num = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name='Страниц'
    )
    available = models.BooleanField(default=True, verbose_name='Доступность')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
