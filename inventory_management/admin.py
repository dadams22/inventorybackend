from django.contrib import admin
from .models import Site, Profile, InventoryItem, Scale, Measurement


admin.site.register(Site)
admin.site.register(Profile)
admin.site.register(InventoryItem)
admin.site.register(Scale)
admin.site.register(Measurement)
