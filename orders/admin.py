from django.contrib import admin
from .models import Order, OrderDetails

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'code', 'price', 'quantity', 'get_user', 'get_order_id']
    list_display_links = ['code','product']
    list_filter = ['order']
    search_fields = ['order__id']  # Search by username and order ID

    def get_user(self, obj):
        return obj.order.user.username

    get_user.short_description = 'User'  # Set a user-friendly column header for user

    def get_order_id(self, obj):
        return obj.order.id

    get_order_id.short_description = 'Order ID'  # Set a user-friendly column header for order ID

admin.site.register(Order)
admin.site.register(OrderDetails, OrderDetailsAdmin)
