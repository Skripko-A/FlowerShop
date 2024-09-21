from django.contrib import admin
from django.utils.html import format_html

from shop.models import (
    Bouquet,
    Order,
    OrderedBouquet,
    Store,
    Event,
    Person,
    Price_range,
    Consultation,
    ConsultationRequest
)


IMAGE_PREVIEW_WIDTH = '300px'
IMAGE_PREVIEW_HEIGHT = '200px'


# Register your models here.
class OrderedBouquetInline(admin.TabularInline):
    model = OrderedBouquet
    extra = 0


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'price', 'picture', 'recomend', 'get_preview', 'events', 'composition', 'size']
    search_fields = [
        'title',
        'recomend',
    ]
    list_display = [
        'title',
        'recomend',
        'get_preview'
    ]
    list_filter = ('events', 'recomend', )
    readonly_fields = ['get_preview']

    def get_preview(self, img):
        return format_html('<img src="{}" style="max-width:{}; max-height:{}"/>',
                           img.picture.url, IMAGE_PREVIEW_WIDTH, IMAGE_PREVIEW_HEIGHT)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
    ]
    list_display = [
        'title',
    ]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    search_fields = [
        'phone',
        'address',
    ]
    list_display = [
        'phone',
        'address',
    ]


@admin.register(Price_range)
class Price_rangeAdmin(admin.ModelAdmin):
    list_display = [
        'price_min',
        'price_max',
    ]


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    search_fields = [
        'create_time',
        'client',
        'consultation_status',
    ]
    list_display = [
        'create_time',
        'client',
        'consultation_status',
    ]
    readonly_fields = [
        'create_time',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'create_time',
        'client',
        'order_status',
    ]
    list_display = [
        'delivery_date',
        'delivery_time',
        'create_time',
        'client',
        'order_status',
    ]
    inlines = [
        OrderedBouquetInline,
    ]


@admin.register(OrderedBouquet)
class OrderedBouquetAdmin(admin.ModelAdmin):
    search_fields = [
        'order',
        'bouquet',
        'quantity',
    ]
    list_display = [
        'order',
        'bouquet',
        'quantity',
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'tm_id', 'role')
#    readonly_fields = ('name', 'phone', 'tm_id', 'role')


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_closed', )
    list_filter = ('is_closed', )
    search_fields = ('phone', )
