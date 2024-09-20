from django.contrib import admin

# Register your models here.
from flower_store.models import Order, Bouquet, Person, Occasion, Price_range, Store, Flower, BouquetFlower

class BouquetFlowerInline(admin.TabularInline):
    model = BouquetFlower
    extra = 1  # Number of extra blank forms to display
    verbose_name = "цветы в букете"
    verbose_name_plural = "цветы в букете"

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    inlines = [BouquetFlowerInline]

admin.site.register(Order)
# admin.site.register(Bouquet)
admin.site.register(Person)
admin.site.register(Occasion)
admin.site.register(Price_range)
admin.site.register(Store)
admin.site.register(Flower)
admin.site.register(BouquetFlower)

