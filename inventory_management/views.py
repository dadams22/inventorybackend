from django.shortcuts import render
from rest_framework import viewsets
from .models import Site, InventoryItem, Scale, ScaleReading
from .serializers import SiteSerializer, InventoryItemSerializer, ScaleSerializer, ScaleReadingSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

    def get_queryset(self):
        user = self.request.user
        site = user.profile.site
        return self.queryset.filter(site=site)

    def perform_create(self, serializer):
        user = self.request.user
        site = user.profile.site
        serializer.save(site=site)


class ScaleViewSet(viewsets.ModelViewSet):
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer

    def get_queryset(self):
        user = self.request.user
        site = user.profile.site
        return self.queryset.filter(site=site)


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def get_queryset(self):
        user = self.request.user
        site = user.profile.site
        return self.queryset.filter(pk=site.pk)


class ScaleReadingViewSet(viewsets.ModelViewSet):
    queryset = ScaleReading.objects.all()
    serializer_class = ScaleReadingSerializer

    def get_queryset(self):
        user = self.request.user
        site = user.profile.site
        return self.queryset.filter(scale__site=site)
