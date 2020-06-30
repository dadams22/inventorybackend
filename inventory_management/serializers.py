from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Site, InventoryItem, Scale, ItemMeasurement


class ItemMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMeasurement
        fields = ('value', 'timestamp')
        read_only_fields = ('value', 'timestamp')


class InventoryItemSerializer(serializers.ModelSerializer):
    scales = serializers.PrimaryKeyRelatedField(many=True, queryset=Scale.objects.all())
    last_measurement = ItemMeasurementSerializer(many=False, read_only=True, source='get_last_measurement')

    class Meta:
        model = InventoryItem
        fields = (
            'id',
            'name',
            'description',
            'scales',
            'created_at',
            'site',
            'last_measurement',
        )
        read_only_fields = (
            'created_at',
            'site',
            'last_measurement',
        )


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = '__all__'
        read_only_fields = ('id', 'site')


class SiteSerializer(serializers.ModelSerializer):
    items = InventoryItemSerializer(many=True)
    scales = ScaleSerializer(many=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'created_at', 'items', 'scales')
        read_only_fields = ('id', 'created_at')
