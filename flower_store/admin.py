from django.contrib import admin

# Register your models here.
from flower_store.models import Order, Bouquet, Person, Occasion, Price_range, Store

admin.site.register(Order)
admin.site.register(Bouquet)
admin.site.register(Person)
admin.site.register(Occasion)
admin.site.register(Price_range)
admin.site.register(Store)

