from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderProductQuerySet(models.QuerySet):
    def calculate_orders_cost(self):
        return self.annotate(total_price=Sum(F('elements__quantity') * F('elements__price')))


class Order(models.Model):
    ACCEPT = 'AC'
    ASSEMBLY = 'AS'
    DELIVERY = 'DL'
    FINISH = 'FN'
    ELECTRONIC_PAY = 'EL'
    CASH_PAY = 'CS'
    UNKNOWN = 'UN'
    STATUS_ORDER_CHOICES = [
        (ACCEPT, 'Принят'),
        (ASSEMBLY, 'Сборка'),
        (DELIVERY, 'Доставка'),
        (FINISH, 'Завершен')
    ]
    PAY_METHOD_CHOICES = [
        (ELECTRONIC_PAY, 'Электронными'),
        (CASH_PAY, 'Наличными'),
        (UNKNOWN, 'Не назначено')
    ]
    products = models.ManyToManyField(
        Product,
        related_name='orders',
        through='OrderElement',
        verbose_name='Продукты'
    )
    cooks_restaurant = models.ForeignKey(
        Restaurant,
        related_name='cook_orders',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Готовит ресторан'
    )
    firstname = models.CharField(
        'Имя',
        max_length=200
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=200
    )
    phonenumber = PhoneNumberField(
        'Телефон'
    )
    address = models.CharField(
        'Адрес доставки',
        max_length=200
    )
    pay_method = models.CharField(
        max_length=2,
        choices=PAY_METHOD_CHOICES,
        default=UNKNOWN,
        verbose_name='Способ оплаты',
        db_index=True
    )
    comment = models.TextField(
        'Комментарий',
        blank=True
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Создан',
        db_index=True
    )
    called_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата звонка',
        db_index=True
    )
    delivered_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата доставки',
        db_index=True
    )
    order_status = models.CharField(
        max_length=2,
        choices=STATUS_ORDER_CHOICES,
        default=ACCEPT,
        verbose_name='Статус заказа',
        db_index=True
    )

    objects = OrderProductQuerySet.as_manager()

    class Meta:
        ordering = ['order_status', '-created_at']
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'


class OrderElement(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='заказ',
        related_name='elements',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='товар',
        related_name='elements',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)],
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f'''
        {self.product.name}, {self.order.firstname}
        {self.order.lastname} {self.order.address}
        '''
