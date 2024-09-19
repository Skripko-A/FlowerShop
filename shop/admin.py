from django.contrib import admin
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
from shop.image_preview import image_preview


# Register your models here.
class OrderedBouquetInline(admin.TabularInline):
    model = OrderedBouquet
    extra = 0


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'price', 'picture', 'recomend', 'preview', 'events']
    search_fields = [
        'title',
        'recomend',
    ]
    list_display = [
        'title',
        'recomend',
    ]
    readonly_fields = ['preview']

    def preview(self, obj):
        return image_preview(obj)


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
