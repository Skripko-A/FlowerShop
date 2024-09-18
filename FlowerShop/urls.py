from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from FlowerShop.views import show_card, show_catalog, show_consultation, show_main, show_delivery, show_payment, show_quiz, show_quiz_step, show_result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_main, name='main'),
    path('catalog', show_catalog, name='catalog'),
    path('delivery', show_delivery, name='delivery'),
    path('card', show_card, name='card'),
    path('consultation', show_consultation, name='consultation'),
    path('payment', show_payment, name='payment'),
    path('quiz', show_quiz, name='quiz'),
    path('quiz_step', show_quiz_step, name='quiz_step'),
    path('result', show_result, name='result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)