from django.shortcuts import render
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
    context = {}
    return render(request, 'catalog.html', context)


def show_delivery(request):
    context={}
    return render(request, 'delivery.html', context)


def show_card(request):
    context={}
    return render(request, 'card.html', context)

def show_consultation(request):
    context={}
    return render(request, 'consultation.html', context)


def show_payment(request):
    context = {}
    return render(request, 'payment.html', context)


def show_quiz(request):
    context = {}
    return render(request, 'quiz.html', context)


def show_quiz_step(request):
    context = {}
    return render(request, 'quiz-step.html', context)


def show_result(request):
    context = {}
    return render(request, 'result.html', context)