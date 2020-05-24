from django.db import models


class Site(models.Model):
    """ Represents a single customer site/restaurant """
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    """ Represents an item in a customer's inventory """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    associated_site = models.ForeignKey(Site, related_name='items', on_delete=models.CASCADE)
    last_measurement = models.FloatField(null=True, blank=True)
    last_measurement_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Scale(models.Model):
    """ Represents a scale that can be used for measurements """
    site = models.ForeignKey(Site, related_name='scales', null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(InventoryItem, related_name='scales', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Scale %d' % self.id


class Measurement(models.Model):
    """ Represents a single measurement made by a single scale """
    value = models.FloatField()
    scale = models.ForeignKey(Scale, on_delete=models.PROTECT)
