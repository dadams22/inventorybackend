from django.shortcuts import render
from rest_framework import viewsets
from .models import Site
from .serializers import SiteSerializer


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
