from django.contrib import admin
from .models import Child, Product
# Register your models here.


admin.site.register(Product)

class ChildAdmin(admin.ModelAdmin):
    list_display = ['code',"name", 'price','is_active','product']
    list_display_links= ['code','name']
    list_filter = ['product','is_active']
    list_editable= ['price', 'is_active']
    search_fields = ('name', 'code', 'details')

# Assuming your 'Child' model is defined in models.py and imported above.
admin.site.register(Child, ChildAdmin)