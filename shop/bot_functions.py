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
from shop.management.commands.bot import main_florist


def send_message_of_consultation(name, tel):
    florist = Person.objects.filter(role='03').first()
    msg = bot.send_message(
        chat_id=florist.tm_id,
        text=f'Доброго дня.\n'
        f'Поступила заявка на консультацию от покупателя по имени {name}, телефон {tel}.',
        reply_markup=main_florist
    )


def send_message_of_new_order(name, tel, order_num):
    print('order message to florist')
    florist = Person.objects.filter(role='03').first()
    bot.send_message(
        chat_id=florist.tm_id,
        text=f'Доброго дня.\n'
        f'Создан заказ номер { order_num } от покупателя по имени {name}, телефон {tel}.',
        reply_markup=main_florist
    )
