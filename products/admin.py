from django.contrib import admin
from .models import Child, Product
# Register your models here.


admin.site.register(Product)

class ChildAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code', 'details')

# Assuming your 'Child' model is defined in models.py and imported above.
admin.site.register(Child, ChildAdmin)
