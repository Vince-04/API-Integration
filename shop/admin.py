from django.contrib import admin
from django.db import models
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "created")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "inventory", "is_active", "created")
    list_filter = ("category", "is_active", "created")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("inventory", "is_active")
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'inventory', 'is_active')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    actions = ['increase_inventory', 'decrease_inventory']
    
    def increase_inventory(self, request, queryset):
        """Action to increase inventory by 10 for selected products"""
        updated = queryset.update(inventory=models.F('inventory') + 10)
        self.message_user(request, f'Successfully increased inventory for {updated} products.')
    increase_inventory.short_description = "Increase inventory by 10"
    
    def decrease_inventory(self, request, queryset):
        """Action to decrease inventory by 5 for selected products"""
        updated = queryset.update(inventory=models.F('inventory') - 5)
        self.message_user(request, f'Successfully decreased inventory for {updated} products.')
    decrease_inventory.short_description = "Decrease inventory by 5"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "status", "paid", "total_amount", "user", "guest_email")
    list_filter = ("status", "paid", "created")
    inlines = [OrderItemInline]
