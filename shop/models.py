from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class OrderedBouquet(models.Model):
    order = models.ForeignKey(
        'Order',
        related_name='ordered_bouquets',
        verbose_name='заказы',
        null=True,
        on_delete=models.SET_NULL,
    )
    bouquet = models.ForeignKey(
        'Bouquet',
        related_name='ordered_bouquets',
        verbose_name='букеты',
        null=True,
        on_delete=models.SET_NULL,
    )
    quantity = models.IntegerField(verbose_name='Количество букетов', default=1)


class Consultation(models.Model):
    STATUSES = (
        ('01', 'Оформлена'),
        ('02', 'Обработана'),
    )
    client = models.ForeignKey(
        'Person',
        verbose_name='клиент',
        related_name='consultations',
        null=True,
        on_delete=models.SET_NULL,
    )
    create_time = models.DateTimeField(
        verbose_name='время создания',
        auto_now_add=True
    )
    consultation_status = models.CharField(
        verbose_name='статус консультации',
        max_length=2,
        choices=STATUSES,
        default='01',
    )

    def get_status(self):
        statuses = {
            '01': 'Оформлена',
            '02': 'Обработана',
        }
        return statuses[self.consultation_status]


class Order(models.Model):
    TIME_PERIODS = (
        ('01', 'Как можно скорее'),
        ('02', '10:00-12:00'),
        ('03', '12:00-14:00'),
        ('04', '14:00-16:00'),
        ('05', '16:00-18:00'),
        ('06', '18:00-20:00'),
    )
    STATUSES = (
        ('01', 'Оформлен'),
        ('02', 'Оплачен'),
        ('03', 'В доставке'),
        ('04', 'Доставлен'),
    )
    client = models.ForeignKey(
        'Person',
        verbose_name='клиент',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL,
    )
    bouquet = models.ManyToManyField(
        'Bouquet',
        through='OrderedBouquet',
        verbose_name='букеты',
        related_name='orders',
    )
    comment = models.TextField(
        'комментарий к заказу',
        blank=True,
    )
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4'
     )
    order_price = models.DecimalField(
        max_digits=19,
        verbose_name='Сумма заказа',
        decimal_places=2,
    )
    create_time = models.DateTimeField(
        verbose_name='время создания',
        auto_now_add=True
    )
    delivery_date = models.DateField(
        verbose_name='дата доставки',
        blank=True
    )
    delivery_time = models.CharField(
        verbose_name='время доставки',
        max_length=2,
        choices=TIME_PERIODS,
        blank=True,
    )
    order_status = models.CharField(
        verbose_name='статус заказа',
        max_length=2,
        choices=STATUSES,
        default='01',
    )

    def __str__(self):
        delivery_date = str(self.delivery_date)
        delivery_period = dict(self.TIME_PERIODS)[self.delivery_time]
        order_status = dict(self.STATUSES)[self.order_status]
        return f'{delivery_date} - {delivery_period} ({order_status})'

    def get_price(self):
        ordered_bouquets = self.ordered_bouquets.all()
        total = 0
        for order in ordered_bouquets:
            price = order.bouquet.get_price() * order.quantity
            total += price

        return total

    def get_status(self):
        statuses = {
            '01': 'Оформлен',
            '02': 'Оплачен',
            '03': 'В доставке',
            '04': 'Доставлен',
        }
        return statuses[self.order_status]

    def get_time(self):
        time_periods = {
            '01': 'Как можно скорее',
            '02': '10:00-12:00',
            '03': '12:00-14:00',
            '04': '14:00-16:00',
            '05': '16:00-18:00',
            '06': '18:00-20:00',
        }
        return time_periods[self.delivery_time]


class Person(models.Model):
    ROLES = (
        ('01', 'Клиент'),
        ('02', 'Курьер'),
        ('03', 'Флорист'),
    )
    name = models.CharField('Имя', max_length=200)
    phone = PhoneNumberField(verbose_name='Телефон', region='RU', db_index=True, unique=True)
    tm_id = models.CharField('ID Телеграм', blank=True, null=True, max_length=20)
    role = models.CharField(
        verbose_name='статус персоны',
        max_length=2,
        choices=ROLES,
        default='01',
    )

    def __str__(self):
        return self.name


class BouquetManager(models.Manager):
    def get_catalog(self, qt_in_row=3):
        bouquet_list = []
        row = []
        for bouquet in Bouquet.objects.all():
            if len(row) == qt_in_row:
                bouquet_list.append({
                    'bouquets_row': row,
                })
                row = []
            row.append(bouquet)
        if len(row) != 0:
            bouquet_list.append({
                    'bouquets_row': row,
            })
        return bouquet_list

    def get_recommended(self):
        return Bouquet.objects.filter(recomend=True)

    def get_by_event(self, event):
        return Bouquet.objects.filter(events=Event.objects.filter(pk=event).first())

    def get_by_price_range(self, range):
        range = Price_range.objects.get(pk=range)
        price_min = range.price_min
        price_max = range.price_max
        if price_max == price_min == 0:
            return Bouquet.objects.all()
        if price_max == 0:
            return Bouquet.objects.filter(price__gte=price_min)
        return Bouquet.objects.filter(price__range=(price_min, price_max))


class Bouquet(models.Model):
    title = models.CharField('название букета', max_length=200, blank=True)
    description = models.TextField(
        'описание букета',
        blank=True,
    )
    composition = models.TextField(
        'состав букета',
        blank=True,
    )
    size = models.TextField(
        'размер букета',
        blank=True,
    )
    picture = models.ImageField(
        verbose_name='изображение букета',
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        max_digits=19,
        verbose_name='Цена букета',
        decimal_places=2,
    )
    recomend = models.BooleanField('рекомендуемый букет', default=False)
    events = models.ManyToManyField(
        'Event',
        verbose_name='события',
        related_name='bouquets',
    )
    objects = BouquetManager()

    def __str__(self):
        return f'торт {self.title} ({self.pk})'


class Event(models.Model):
    title = models.CharField(
        verbose_name='Событие',
        max_length=32,
    )

    def __str__(self):
        return f'{str(self.title)}'


class Store(models.Model):
    phone = models.CharField('Телефон магазина', max_length=12, unique=True)
    address = models.TextField(
        'Адрес магазина',
        help_text='ул. Подольских курсантов д.5 кв.4'
     )

    def __str__(self):
        return f'{self.address}({self.phone})'


class Price_rangeManager(models.Manager):
    def get_sort_ranges(self):
        return Price_range.objects.all().order_by('price_min')


class Price_range(models.Model):
    price_min = models.DecimalField(
        max_digits=19,
        verbose_name='Цена минимум',
        decimal_places=2,
    )
    price_max = models.DecimalField(
        max_digits=19,
        verbose_name='Цена максимум',
        decimal_places=2,
    )
    objects = Price_rangeManager()

    def get_text(range):
        if range.price_min == 0 and range.price_max == 0:
            text = 'Не имеет значения'
        elif range.price_min == 0:
            text = f'До {range.price_max} руб'
        elif range.price_max == 0:
            text = f'от {range.price_min} руб'
        else:
            text = f'{range.price_min} - {range.price_max} руб'
        return text


class ConsultationRequest(models.Model):
    name = models.CharField(
        verbose_name='Имя', 
        max_length=25
        )
    phone = PhoneNumberField(
        verbose_name='Номер телефона', 
        region='RU', 
        db_index=True
        )
    is_closed = models.BooleanField(verbose_name='Обработана?', default='False')

    class Meta:
        verbose_name = 'Заявка на консультацию'
        verbose_name_plural = 'Заявки на консультацию'

    def __str__(self):
        return f'{self.name}, т. {self.phone}'