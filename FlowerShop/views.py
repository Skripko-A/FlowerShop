from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlencode
from shop.models import (
    Bouquet,
    Order,
    OrderedBouquet,
    Store,
    Event,
    Person,
    Price_range,
    Consultation,
)
import datetime


def show_main(request):
    context = {
        'bouquets_recommended': Bouquet.objects.get_recommended(),
        'stores': Store.objects.all(),
    }
    return render(request, 'index.html', context)


def show_catalog(request):
    context = {
        'bouquets_rows': Bouquet.objects.get_catalog(3)
    }
    return render(request, 'catalog.html', context)


def show_delivery(request):
    button_value = request.POST.get('button_value')
    time_periods = []
    for period in Order.TIME_PERIODS:
        time_periods.append({
            'id': period[0],
            'text': period[1],
        })
    context = {
        'time_periods': time_periods,
        'bouquet_id': button_value,
    }
    return render(request, 'delivery.html', context)


def show_card(request):
    context={}
    return render(request, 'card.html', context)


def show_consultation(request):
    if request.GET:
        if 'fname' in request.GET.keys() or 'tel' in request.GET.keys():
            if request.GET['fname'] and request.GET['tel']:
                pass
                #print(request.GET['fname'])
                #print(request.GET['tel'])
                # TODO отправить сообщение флористу
                # TODO сообщить посетителю, что зпрос отправлен и с ним свяжутся
    context = {}
    return render(request, 'consultation.html', context)


def show_payment(request):
    name = request.POST.get('fname')
    phone = request.POST.get('tel')
    address = request.POST.get('address')
    order_time = request.POST.get('orderTime')

    context = {
        'name': name,
        'phone_number': phone,
        'address': address,
        'order_time': order_time,
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


def process_payment(request):
    if request.method == 'POST':
        name = request.POST.get('fname')
        phone_number = request.POST.get('tel')
        address = request.POST.get('address')
        order_time = request.POST.get('orderTime')
        card_num = request.POST.get('cardNum')
        card_mm = request.POST.get('cardMm')
        card_gg = request.POST.get('cardGg')
        card_fname = request.POST.get('cardFname')
        card_cvc = request.POST.get('cardCvc')
        email = request.POST.get('mail')

        if validate_card_number(card_num):
            client, created = Person.objects.get_or_create(
                phone=phone_number,
                defaults={'name': name, 'role': '01'},
            )

            if not created and client.name != name:
                client.name = name
                client.save()

            order = Order.objects.create(
                client=client,
                address=address,
                delivery_date=datetime.date.today() + datetime.timedelta(days=1),
                delivery_time=order_time,
                order_price=0,
            )

            # TODO вероятно тут послать сообщение флористу/курьеру

            messages.success(request, 'Заказ оформлен!')
            return redirect('main')
        else:
            messages.error(request, 'Платеж не прошел. Проверьте информацию')
            return redirect('payment')

    return redirect('payment')


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
