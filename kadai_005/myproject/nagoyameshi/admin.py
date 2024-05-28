from django.contrib import admin
from .models import Store, Booking, Date, Review, Product
# Register your models here.

admin.site.register(Store)
admin.site.register(Booking)
admin.site.register(Date)
admin.site.register(Review)
admin.site.register(Product)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('shop_id', 'shop_name', 'user', 'score')
    list_display_links = ('shop_name',)
    list_editable = ('score',)