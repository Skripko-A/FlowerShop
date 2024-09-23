from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import CharField, Serializer,ValidationError, ModelSerializer, ListField
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
from shop.bot_functions import send_message_of_consultation, send_message_of_new_order

import datetime


def show_main(request):
    context = {
        'bouquets_recommended': Bouquet.objects.get_recommended(),
        'stores': Store.objects.all(),
        'current_year': datetime.date.today().year,
    }
    return render(request, 'index.html', context)


def show_catalog(request):
    context = {
        'bouquets_rows': Bouquet.objects.get_catalog(3)
    }
    return render(request, 'catalog.html', context)


def show_delivery(request):
    bouquet_id = request.POST.get('bouquet_id')
    time_periods = []
    for period in Order.TIME_PERIODS:
        time_periods.append({
            'id': period[0],
            'text': period[1],
        })
    context = {
        'time_periods': time_periods,
        'bouquet_id': bouquet_id,
    }
    return render(request, 'delivery.html', context)


def show_card(request):
    context={}
    return render(request, 'card.html', context)


def show_consultation(request):
    if request.GET:
        if 'fname' in request.GET.keys() or 'tel' in request.GET.keys():
            if request.GET['fname'] and request.GET['tel']:
                fname = request.GET['fname']
                tel = request.GET['tel']
                ConsultationRequest.objects.create(
                    name=fname,
                    phone=tel,
                )

                new_client, created = Person.objects.get_or_create(
                    phone=tel,
                    defaults={'name': fname}
                )

                if not created and new_client.name != fname:
                    new_client.name = fname
                    new_client.save()

                send_message_of_consultation(fname, tel)
                # TODO отправить сообщение флористу
                # TODO сообщить посетителю, что зпрос отправлен и с ним свяжутся
    context = {}
    return render(request, 'consultation.html', context)


def show_payment(request):
    bouquet_id = request.POST.get('bouquet_id')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    order_time = request.POST.get('delivery_time')

    context = {
        'bouquet_id': bouquet_id,
        'name': name,
        'phone': phone,
        'address': address,
        'delivery_time': order_time,
        'delivery_date': datetime.date.today() + datetime.timedelta(days=1),
    }
    return render(request, 'payment.html', context)


def validate_card_number(card_number):
    # Алгоритм для проверки номера карты
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    checksum = 0
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['address', 'delivery_time']

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'phone']


@api_view(['POST'])
@transaction.atomic
def process_payment(request):
    '''Данные для тестирования:
    http://127.0.0.1:8000/order-register/
    {"name": "Клиентик",
    "phone": "+79876545577",
    "address": "Stalins street 10",
    "delivery_time": "02",
    "bouquet_id": 1,
    "cardNum": "2222111111111111"}'''

    order_serializer = OrderSerializer(data=request.data)
    if Person.objects.filter(phone=request.data['phone']):
        client = Person.objects.get(phone=request.data['phone'])
        if client.name != request.data['name']:
            client.name = request.data['name']
            client.save()
    else:
        client_serializer = ClientSerializer(data=request.data)
        try:
            client_serializer.is_valid(raise_exception=True)
            client = client_serializer.save()
        except ValidationError as e:
            return Response({'errors': e.detail}, status=400)
    print(client)        
    try:
        order_serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        return Response({'errors': e.detail}, status=400)
    address = order_serializer.validated_data['address']
    delivery_time = order_serializer.validated_data['delivery_time']

    bouquet_id = request.data['bouquet_id']
    card_num = request.data['cardNum']

    if not validate_card_number(card_num):
        raise ValidationError

    new_order = Order.objects.create(
        client=client,
        address=address,
        delivery_date=datetime.date.today() + datetime.timedelta(days=1),
        delivery_time=delivery_time,
        order_price=0,
        bouquet=Bouquet.objects.get(pk=bouquet_id),
    )
    messages.success(request, 'Заказ оформлен!')
    return Response({'success': True, 'redirect_url': 'main'}, status=201)
    #return redirect('main')
       # TODO вероятно тут послать сообщение флористу/курьеру


def show_pay_delivery(request):
    time_periods = []
    for period in Order.TIME_PERIODS:
        time_periods.append({
            'id': period[0],
            'text': period[1],
        })

    bouquet_id = request.POST.get('bouquet_id')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    order_time = request.POST.get('delivery_time')

    context = {
        'bouquet_id': bouquet_id,
        'name': name,
        'phone': phone,
        'address': address,
        'time_periods': time_periods,
        'delivery_time': order_time,
        'delivery_date': datetime.date.today() + datetime.timedelta(days=1),
    }
    return render(request, 'pay_delivery.html', context)


def show_quiz(request):
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'quiz.html', context)


def show_quiz_step(request):
    button_value = request.POST.get('button_value')
    request.session['event_id'] = button_value

    price_ranges = Price_range.objects.all()

    context = {
        'price_ranges': price_ranges,
    }
    return render(request, 'quiz-step.html', context)


def show_result(request):
    if request.GET:
        fname = ''
        tel = ''
        if 'fname' in request.GET.keys() or 'tel' in request.GET.keys():
            if request.GET['fname'] and request.GET['tel']:
                fname = request.GET['fname']
                tel = request.GET['tel']
                params = {
                    'fname': fname,
                    'tel': tel,
                }
#                send_message_of_consultation(fname, tel)
                # TODO отправить сообщение флористу
                # TODO сообщить посетителю, что зпрос отправлен и с ним свяжутся
        return redirect('{}?{}'.format(reverse(show_consultation), urlencode(params)))
    if not request.session['event_id'] or not request.POST:
        return redirect(show_main)
    event_id = request.session['event_id']
    if request.POST:
        button_value = request.POST.get('button_value')
        request.session['price_range_id'] = button_value

        # TODO случай, если букета нет (мб в верстке захардкодить)
        result = Bouquet.objects.get_by_event(event_id)
        result = result & Bouquet.objects.get_by_price_range(request.session['price_range_id'])

        context = {
            'result': result.first(),
            'stores': Store.objects.all(),
        }
    return render(request, 'result.html', context)


class ConsultationRequestSerializer(ModelSerializer):
    class Meta:
        model = ConsultationRequest
        fields = ['name', 'phone']


@api_view(['POST',])
@csrf_exempt
@transaction.atomic
def register_consultation_request(request):
    '''
    Данные для тестирования http://127.0.0.1:8000/consultation-request/

    {"name": "Иван", "phone": "+79998887766"}
    '''
    serializer = ConsultationRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    name = serializer.validated_data['name']
    phone = serializer.validated_data['phone']

    ConsultationRequest.objects.create(
        name=name,
        phone=phone,
        )

    new_client, created = Person.objects.get_or_create(
        phone=phone,
        defaults={'name': name}
    )

    if not created and new_client.name != name:
        new_client.name = name
        new_client.save()

    return Response(serializer.data, status=201)
