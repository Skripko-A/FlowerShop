from django.contrib import admin
from django.urls import path

from FlowerShop.views import show_catalog, show_main, show_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_main, name='show_main'),
    path('catalog', show_catalog, name='show_catalog'),
    path('order', show_order, name='show_order')
]
