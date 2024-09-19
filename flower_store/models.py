from django.db import models
from datetime import datetime

# Create your models here.



class Occasion(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование причины",
    )

    class Meta:
        verbose_name = 'причина'
        verbose_name_plural = 'причины'

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    CUSTOMER = 'customer'
    COURIER = 'courier'
    FLORIST = 'florist'

    ROLES = [
        (CUSTOMER, 'Покупатель'),
        (COURIER, 'Курьер'),
        (FLORIST, 'Флорист'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Имя",
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
    )
    telegram_id = models.CharField(
        max_length=100,
        verbose_name="id в телеграме",
    )
    role = models.CharField(
        max_length=15,
        verbose_name="Статус",
        choices=ROLES,
        default=CUSTOMER,
    )

    class Meta:
        verbose_name = 'человек'
        verbose_name_plural = 'люди'

    def __str__(self):
        return f"{self.name}: {self.role}"


class Flower(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
    )

    class Meta:
        verbose_name = 'цветок'
        verbose_name_plural = 'цветы'

    def __str__(self):
        return f"{self.name}"


class Bouquet(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название букета",
    )
    description = models.CharField(
        max_length=100,
        verbose_name="Описание букета",
    )
    size = models.CharField(
        max_length=100,
        verbose_name="Описание размеров",
    )
    price = models.IntegerField(
        "Цена в руб."
    )
    occasion = models.ManyToManyField(
        Occasion,
        verbose_name="Событие",
        related_name="bouquets",
        blank=True,
    )
    flowers = models.ManyToManyField(
        Flower, through='BouquetFlower'
    )

    class Meta:
        verbose_name = 'букет'
        verbose_name_plural = 'букеты'

    def __str__(self):
        return f"{self.name}: {self.price}"


class BouquetFlower(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'цветы в букете'
        verbose_name_plural = 'цветы в букете'

    def __str__(self):
        return f'{self.quantity} x {self.flower.name} in {self.bouquet.name}'


class Price_range(models.Model):
    low = models.IntegerField(
        "Нижняя граница",
        default=0,
    )
    high = models.IntegerField(
        "Верхняя граница",
        default=0,
    )

    class Meta:
        verbose_name = 'бюджет'
        verbose_name_plural = 'бюджеты'

    def __str__(self):
        return f"{self.low} - {self.high}"


class Order(models.Model):
    CREATED = 'created'
    PAID = 'paid'
    PROCESSED = 'processed'
    DELIVERY = 'being_delivered'

    ORDER_STATUSES = [
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (PROCESSED, 'Собран'),
        (DELIVERY, 'Передан в доставку'),
    ]

    date = models.DateTimeField(
        default=datetime.now,
        blank=True,
        verbose_name="Дата и время заказа",
    )
    customer = models.ForeignKey(
        Person,
        verbose_name="Покупатель",
        related_name="Customer",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUSES,
        default=CREATED,
    )
    bouquet = models.ManyToManyField(
        Bouquet,
        verbose_name="Букет",
        related_name="orders",
        blank=True,
    )
    address = models.CharField(
        max_length=100,
        verbose_name="Адрес доставки",
    )
    delivery_time = models.TimeField(
        verbose_name="Время доставки",
    )
    # TODO Do we need another phone?
    phone = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
    )
    commentary = models.TextField(
        "Комментарии к заказу",
    )
    courier = models.ForeignKey(
        Person,
        verbose_name="Курьер",
        related_name="Courier",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f"{self.customer.name}: {self.bouquet.name}"


class Store(models.Model):
    address = models.TextField(
        "Адрес",
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
    )

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'

    def __str__(self):
        return f"{self.address}"
