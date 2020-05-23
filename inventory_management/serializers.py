from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Site, InventoryItem


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'
        read_only_fields = ('created_at',)


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ('id', 'name', 'description', 'created_at', 'last_measurement', 'last_measurement_timestamp')
        read_only_fields = ('created_at', 'last_measurement', 'last_measurement_timestamp')
