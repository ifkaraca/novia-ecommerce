from django.contrib import admin
from .models import Category,Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug",)
    search_fields = ["name"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","category","price","discount_rate","stock","is_active","vendor",)
    list_filter = ("category",)
    search_fields = ["name"] 

