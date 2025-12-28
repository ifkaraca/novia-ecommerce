from django.contrib import admin
from .models import (
    Category,
    Product,
    Vendor,
    Attribute,
    AttributeValue,
    ProductImages,
    ProductVariant)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug","parent","icon_class",)
    search_fields = ["name"]
    prepopulated_fields = {"slug":('name',)}
    list_filter = ("parent",)

class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]
    list_display = ("name",)

class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 3 # Varsayılan 3 boş resim alanı açar

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    # Varyasyon özelliklerini (Kırmızı + XL) seçmek için:
    filter_horizontal = ('attribute_values',) 
    # Not: Eğer seçim kutusu çok geniş gelirse bu satırı silip tekrar dene.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","category","price","discount_rate","is_active","vendor",)
    list_filter = ("category","vendor","is_active")
    search_fields = ["name"]
    prepopulated_fields = {"slug":('name',)}
    inlines = [ProductVariantInline, ProductImageInline]

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("user","name","is_active","created_at")
    search_fields = ['name']
    list_filter = ("is_active",)
