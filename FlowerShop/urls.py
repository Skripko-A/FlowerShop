from django.contrib import admin
from django.urls import path

from FlowerShop.views import show_main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_main, name='show_main'),
]
