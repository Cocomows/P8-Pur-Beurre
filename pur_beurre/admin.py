from django.contrib import admin
from .models import Product, Save

# Register your models here.


admin.site.register(Product)


@admin.register(Save)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('date', 'saved_by')
