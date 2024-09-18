from django.shortcuts import render


def show_main(request):
    context={}
    return render(request, 'index.html', context)


def show_catalog(request):
    context={}
    return render(request, 'catalog.html', context)


def show_order(request):
    context={}
    return render(request, 'order.html', context)


def show_card(request):
    context={}
    return render(request, 'card.html', context)

def show_consultation(request):
    context={}
    return render(request, 'consultation.html', context)