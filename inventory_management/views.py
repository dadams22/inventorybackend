from django.shortcuts import render
from rest_framework import viewsets
from .models import Site, InventoryItem
from .serializers import SiteSerializer, InventoryItemSerializer


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
