from shop.management.commands.bot import bot, payload
from shop.models import (
    Bouquet,
    Order,
    OrderedBouquet,
    Store,
    Event,
    Person,
    Price_range,
    ConsultationRequest,
)
from shop.management.commands.bot import markup_florist


def send_message_of_consultation(name, tel):
    florist = Person.objects.filter(role='03').first()
    msg = bot.send_message(
        chat_id=florist.tm_id,
        text=f'Доброго дня.\n'
        f'Поступила заявка на консультацию от покупателя по имени {name}, телефон {tel}.',
        reply_markup=markup_florist
    )


def send_message_of_new_order(name, tel, order_num):
    florist = Person.objects.filter(role='03').first()
    bot.send_message(
        chat_id=florist.tm_id,
        text=f'Доброго дня.\n'
        f'Создан заказ номер { order_num } от покупателя по имени {name}, телефон {tel}.',
        reply_markup=markup_florist
    )


def send_message_of_new_delivery(name, tel, order):
    courier = Person.objects.filter(role='02').first()
    time = order.get_time()
    bot.send_message(
        chat_id=courier.tm_id,
        text=f'Доброго дня.\n'
        f'Pаказ номер { order.id } для покупателя по имени {name}, телефон {tel} собран.\n'
        f'Требуется доставить его по адресу: { order.address }.\n'
        f'Время доставки сегодня { time }.',
    )
