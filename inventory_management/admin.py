from django.contrib import admin
from .models import Site, InventoryItem, Scale, Measurement


admin.site.register(Site)
admin.site.register(InventoryItem)
admin.site.register(Scale)
admin.site.register(Measurement)
