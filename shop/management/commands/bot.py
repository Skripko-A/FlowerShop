import telebot

from threading import Thread
from django.core.management.base import BaseCommand
from django.conf import settings
from environs import Env
from telebot.util import quick_markup
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


env = Env()
env.read_env()

payload = {}
tm_bot_token = env('TM_BOT_TOKEN')
bot = telebot.TeleBot(token=tm_bot_token)

markup_florist = quick_markup({
    'Посмотреть заказы': {'callback_data': 'get_orders'},
    'Посмотреть открытые заявки на консультации': {'callback_data': 'get_open_consultation_requests'},
}, row_width=1)


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


def check_user_in_cache(msg: telebot.types.Message):
    """проверят наличие user в кэше
    это на случай, если вдруг случился сбой/перезапуск скрипта на сервере
    и кэш приказал долго жить. В этом случае нужно отправлять пользователя в начало
    пути, чтобы избежать ошибок """
    user = payload.get(msg.chat.id)
    if not user:
        bot.send_message(msg.chat.id, 'Упс. Что то пошло не так.\n'
                                      'Нажмите /start')
        return None
    else:
        return user


def get_markup(buttons, row_width=1):
    return quick_markup(buttons, row_width=row_width)


def start_bot(message: telebot.types.Message):
    tg_name = message.from_user.username
    payload[message.chat.id] = {
        'tg_name': tg_name,
        'tg_id': message.chat.id,
        'msg_id_1': None,
        'msg_id_2': None,
        'next_menu_name': None,
        'del_message': None,
    }
    msg = bot.send_message(message.chat.id, f'Здравствуйте, {tg_name}')
    payload[message.chat.id]['msg_id_1'] = msg.id
    person = Person.objects.filter(tm_id=message.chat.id).first()

    if person.role == '03':
        msg = bot.send_message(message.chat.id, 'Я бот магазина цветов, \n'
                               'буду присылать вам уведомления \n'
                               'об оформленных заказах и заявках на консультацию.', 
                               reply_markup=markup_florist)
    elif person.role == '01':
        msg = bot.send_message(message.chat.id, 'Привет.', reply_markup=markup_florist)

    payload[message.chat.id]['msg_id_2'] = msg.id
    print(payload)


def menu_florist(message: telebot.types.Message):
    user = payload[message.chat.id]    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=user['msg_id_2'],
        text='Что будем делать?.',
        reply_markup=markup_florist
    )


def get_open_consultation_requests(message: telebot.types.Message):
    user = payload[message.chat.id]
    user['msg_id_2'] = message.id
    user['next_menu_name'] = 'get_open_consultation_request'
    if user['del_message']:
        bot.delete_message(chat_id=message.chat.id, message_id=user['del_message'])
    buttons = {}
    open_consultations = ConsultationRequest.objects.filter(is_closed=False)
    for open_consultation in open_consultations:
        buttons.update({
            f'Клиент: {open_consultation.name} Тел: {open_consultation.phone}': {
                'callback_data': open_consultation.pk,
            }
        })
    buttons.update({'Вернуться в меню': {'callback_data': 'menu_florist'}})
    markup = get_markup(buttons)
    message_text = 'Выберите консультацию'
    if len(open_consultations) == 0:
        message_text = 'Открытых заявок на консультацию нет.'
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=message_text, reply_markup=markup)


def get_orders(message: telebot.types.Message):
    user = payload[message.chat.id]
    user['msg_id_2'] = message.id
    user['next_menu_name'] = 'get_order'
    if user['del_message']:
        bot.delete_message(chat_id=message.chat.id, message_id=user['del_message'])
    buttons = {}
    new_orders = Order.objects.filter(order_status__in=['01', '02'])
    for order in new_orders:
        buttons.update({
            f'Заказ № { order.pk }:\n'
            f'Заказчик {order.client.name}. Тел: {order.client.phone}': {
                'callback_data': order.pk,
            }
        })
    buttons.update({'Вернуться в меню': {'callback_data': 'menu_florist'}})
    markup = get_markup(buttons)
    message_text = 'Выберите заказ:'
    if len(new_orders) == 0:
        message_text = 'Новых заказов нет.'
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=message_text, reply_markup=markup)


def get_open_consultation_request(message: telebot.types.Message, consultation_id):
    user = payload[message.chat.id]
    print(consultation_id)
    user['next_menu_name'] = 'close_consultation'
    buttons = {}
    buttons.update({'Консультация завершена': {'callback_data': consultation_id}})
    buttons.update({'Вернуться в меню': {'callback_data': 'menu_florist'}})
    markup = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Завершить консультацию?', reply_markup=markup)


def get_order(message: telebot.types.Message, order_id):
    user = payload[message.chat.id]
    print(order_id)
    user['next_menu_name'] = 'send_order_to_delivery'
    buttons = {}
    buttons.update({'Отдан в доставку': {'callback_data': order_id}})
    buttons.update({'Вернуться в меню': {'callback_data': 'menu_florist'}})
    markup = get_markup(buttons)
    order = Order.objects.filter(pk=order_id).first()
    bouquet = Bouquet.objects.get(pk=order.bouquet.pk)
    bot.send_photo(
        chat_id=message.chat.id,
        photo=bouquet.picture,
        caption=f'{ bouquet.title }.\n'
            f'Состав:\n'
            f'{ bouquet.composition }'
    )
    msg = bot.send_message(chat_id=message.chat.id,
            text='Отдаем в доставку?', reply_markup=markup)
    user['msg_id_2'] = msg.id


def close_consultation(message: telebot.types.Message, consultation_id):
    user = payload[message.chat.id]
    print(consultation_id)
    user['next_menu_name'] = 'close_consultation'
    consultation = ConsultationRequest.objects.get(pk=consultation_id)
    consultation.is_closed = True
    consultation.save()
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=user['msg_id_2'],
        text='Консультация закрыта.\n'
            'Что будем делать дальше?.',
        reply_markup=markup_florist
    )


def send_order_to_delivery(message: telebot.types.Message, order_id):
    user = payload[message.chat.id]
    user['next_menu_name'] = 'send_order_to_delivery'
    order = Order.objects.filter(pk=order_id).first()
    order.is_closedorder_status = '03'
    order.save()
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=user['msg_id_2'],
        text='Букет заберет курьер.\n'
            'Что будем делать дальше?.',
        reply_markup=markup_florist
    )
    send_message_of_new_delivery(order.client.name, order.client.phone, order)


def get_speaker_buttons(message: telebot.types.Message, call):
    user = payload[message.chat.id]
    buttons = {}
    reports = db_functions.get_reports()
    for report in reports[user['sheet']:user['sheet']+2]:
        name = report.speaker.name
        user['code_reports'].append(str(report.id))
        theme = report.theme
        buttons.update({f'{name} - {theme}': {'callback_data': report.id}})
    user['sheet'] += 2
    if user['sheet'] < len(reports):
        buttons.update({'Еще доклады': {'callback_data': 'choice_speaker'}})
    else:
        user['sheet'] = 0
    buttons.update({'Вернуться в меню': {'callback_data': 'main_menu'}})
    markup = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выберите доклад', reply_markup=markup)


@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    start_bot(message)


@bot.callback_query_handler(func=lambda call: call.data)
def handle_buttons(call):
    user = check_user_in_cache(call.message)
    if not user:
        return
    if call.data == 'get_open_consultation_requests':
        get_open_consultation_requests(call.message)
    elif call.data == 'menu_florist':
        menu_florist(call.message)
    elif user['next_menu_name'] == 'get_open_consultation_request':
        get_open_consultation_request(call.message, call.data)
    elif call.data == 'get_orders':
        get_orders(call.message)
    elif user['next_menu_name'] == 'get_order':
        get_order(call.message, call.data)
    elif user['next_menu_name'] == 'send_order_to_delivery':
        get_order(call.message, call.data)
    elif user['next_menu_name'] == 'close_consultation':
        close_consultation(call.message, call.data)

#bot.polling(none_stop=True, interval=1)

def bot_thread():
    bot.remove_webhook()
    bot.polling(none_stop=True, interval=1)


t = Thread(target=bot_thread)
t.setDaemon(True)
t.start()

