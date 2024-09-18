from django.shortcuts import render


def show_main(request):
    context={}
    return render(request, 'index.html', context)


def show_catalog(request):
    context={}
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