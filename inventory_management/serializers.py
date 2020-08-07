from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Site, InventoryItem, Scale, ItemMeasurement, ScaleReading, ItemStocking


class ItemMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMeasurement
        fields = ('value', 'timestamp')
        read_only_fields = ('value', 'timestamp')


class ItemStockingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemStocking
        fields = ('id', 'created_at',)
        read_only_fields = ('created_at',)


class InventoryItemSerializer(serializers.ModelSerializer):
    stockings = ItemStockingSerializer(many=True, source='get_active_stockings')
    last_measurement = ItemMeasurementSerializer(many=False, read_only=True, source='get_last_measurement')

    class Meta:
        model = InventoryItem
        fields = (
            'id',
            'name',
            'description',
            'stockings',
            'created_at',
            'site',
            'last_measurement',
        )
        read_only_fields = (
            'stockings',
            'created_at',
            'site',
            'last_measurement',
        )


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = '__all__'
        read_only_fields = ('id', 'site',)


class ScaleReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScaleReading
        fields = '__all__'
        read_only_fields = ('timestamp',)


class SiteSerializer(serializers.ModelSerializer):
    items = InventoryItemSerializer(many=True)
    scales = ScaleSerializer(many=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'created_at', 'items', 'scales')
        read_only_fields = ('id', 'created_at',)
