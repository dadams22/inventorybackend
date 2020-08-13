from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Site, InventoryItem, Scale, ItemMeasurement, ScaleReading, ItemStocking


class ItemMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMeasurement
        fields = ('value', 'timestamp')
        read_only_fields = ('value', 'timestamp')


class ItemStockingSerializer(serializers.ModelSerializer):
    scales = serializers.PrimaryKeyRelatedField(many=True, queryset=Scale.objects.all())
    last_measurement = serializers.FloatField(source='get_last_measurement')

    class Meta:
        model = ItemStocking
        fields = ('id', 'created_at', 'scales', 'last_measurement')
        read_only_fields = ('created_at', 'last_measurement')


class InventoryItemSerializer(serializers.ModelSerializer):
    stockings = ItemStockingSerializer(many=True, source='get_active_stockings', read_only=True)
    last_measurement = serializers.FloatField(source='get_last_measurement', read_only=True)

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
            'id',
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
