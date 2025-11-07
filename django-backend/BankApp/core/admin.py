from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Organization, StoreUnit, Receipt, Product, ReceiptItem, ChatSession, ChatMessage

# Odstrániť staré registrácie
# admin.site.register(Users)
# admin.site.register(Organization)
# admin.site.register(Receipt)
# admin.site.register(Products)
# admin.site.register(Product_Category)
# admin.site.register(Products_Items)

# Nové registrácie
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_date', 'last_login_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('registration_date',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'ico', 'dic', 'municipality', 'country')
    search_fields = ('name', 'ico', 'dic')
    list_filter = ('country', 'municipality')
    readonly_fields = ('organization_id',)

@admin.register(StoreUnit)
class StoreUnitAdmin(admin.ModelAdmin):
    list_display = ('unit_id', 'name', 'organization', 'street_name', 'building_number', 'municipality', 'latitude', 'longitude')
    search_fields = ('name', 'street_name', 'organization__name')
    list_filter = ('country', 'municipality', 'organization')
    readonly_fields = ('unit_id',)

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('fs_receipt_id', 'issue_date', 'user', 'organization', 'store_unit', 'total_price')
    search_fields = ('fs_receipt_id', 'user__username', 'organization__name')
    list_filter = ('issue_date', 'organization')
    readonly_fields = ('receipt_id',)
    date_hierarchy = 'issue_date'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'ai_category')
    search_fields = ('name', 'original_name', 'brand', 'category')
    list_filter = ('category', 'ai_category')
    readonly_fields = ('product_id',)

@admin.register(ReceiptItem)
class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'product', 'quantity', 'unit_price', 'total_price')
    search_fields = ('receipt__fs_receipt_id', 'product__name')
    list_filter = ('receipt__organization',)
    readonly_fields = ('receipt_item_id',)

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)  # Pridať filter

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'created_at', 'short_message')
    list_filter = ('sender', 'created_at')
    readonly_fields = ('created_at',)
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'