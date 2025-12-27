from django.contrib import admin
from .models import Category,Product,Vendor

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug","parent",)
    search_fields = ["name"]
    prepopulated_fields = {"slug":('name',)}
    list_filter = ("parent",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","category","price","discount_rate","stock","is_active","vendor",)
    list_filter = ("category",)
    search_fields = ["name"]
    prepopulated_fields = {"slug":('name',)}

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("user","name",)
    search_fields = ['name']