from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Site, InventoryItem, Scale


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ('id', 'name', 'description', 'created_at', 'last_measurement', 'last_measurement_timestamp')
        read_only_fields = ('created_at', 'last_measurement', 'last_measurement_timestamp')


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = '__all__'
        read_only_fields = ('id', 'associated_site')


class SiteSerializer(serializers.ModelSerializer):
    items = InventoryItemSerializer(many=True)
    scales = ScaleSerializer(many=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'created_at', 'items', 'scales')
        read_only_fields = ('id', 'created_at')
