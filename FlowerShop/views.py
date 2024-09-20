from django.shortcuts import render, redirect
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


def show_main(request):
    context = {
        'bouquets_recommended': Bouquet.objects.get_recommended()
    }
    return render(request, 'index.html', context)


def show_catalog(request):
    context = {
        'bouquets_rows': Bouquet.objects.get_catalog(3)
    }
    return render(request, 'catalog.html', context)


def show_delivery(request):
    context={}
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
    context = {}
    return render(request, 'payment.html', context)


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
