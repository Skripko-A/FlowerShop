from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from FlowerShop.views import show_card, show_catalog, show_consultation, show_main, show_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_main, name='main'),
    path('catalog', show_catalog, name='catalog'),
    path('order', show_order, name='order'),
    path('card', show_card, name='card'),
    path('consultation', show_consultation, name='consultation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)