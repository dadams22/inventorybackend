from django.contrib import admin
from .models import Site, Profile, InventoryItem, Scale, ScaleReading


admin.site.register(Site)
admin.site.register(Profile)
admin.site.register(InventoryItem)
admin.site.register(Scale)
admin.site.register(ScaleReading)
