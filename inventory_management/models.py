from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Site(models.Model):
    """ Represents a single customer site/restaurant """
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """ Represents a profile containing extra information about a user """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)


# # TODO: make a signals.py file and move these to there
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class InventoryItem(models.Model):
    """ Represents an item in a customer's inventory """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site, related_name='items', on_delete=models.CASCADE)

    def get_last_measurement(self):
        measurements = filter(
            lambda stocking: stocking.active and stocking.get_last_measurement() is not None,
            [stocking.get_last_measurement() for stocking in self.stockings]
        )

        if not measurements:
            return None

        return sum([measurement.value for measurement in measurements])

    def get_active_stockings(self):
        return ItemStocking.objects.filter(item=self.pk, active=True)

    def __str__(self):
        return self.name


class ItemStocking(models.Model):
    item = models.ForeignKey(InventoryItem, related_name='stockings', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def get_last_measurement(self):
        try:
            result = ItemMeasurement.objects.filter(stocking=self.pk).latest('timestamp').value
        except ItemMeasurement.DoesNotExist:
            result = None
        return result

    def __str__(self):
        return '%s stocking: %s' % (self.item.name, str(self.created_at))


class Scale(models.Model):
    """ Represents a scale that can be used for measurements """
    site = models.ForeignKey(Site, related_name='scales', null=True, on_delete=models.SET_NULL)
    stocking = models.ForeignKey(ItemStocking, related_name='scales', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Scale %d' % self.id


class ScaleReading(models.Model):
    """ Represents a single measurement made by a single scale """
    value = models.FloatField()
    scale = models.ForeignKey(Scale, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Reading: Scale %s at %s' % (self.scale.pk, str(self.timestamp))


class ItemMeasurement(models.Model):
    """
    Represents the measured value for the given item at the specified time.
    This measurement may be the result of multiple different ScaleReadings.
    """
    stocking = models.ForeignKey(ItemStocking, related_name='measurements', on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


# Create an ItemMeasurement object any time a ScaleReading is created
@receiver(post_save, sender=ScaleReading)
def create_item_measurement(sender, instance, created, **kwargs):
    # Only create measurements for new readings
    if not created:
        return

    scale = instance.scale
    stocking = scale.stocking
    linked_scales = Scale.objects.filter(stocking=stocking)

    latest_readings = []
    for scale in linked_scales:
        try:
            reading = ScaleReading.objects.filter(scale=scale, timestamp__gt=stocking.created_at).latest('timestamp')
            latest_readings.append(reading)
        except ScaleReading.DoesNotExist:
            pass

    if len(latest_readings) < len(linked_scales):
        return

    total_value = sum([reading.value for reading in latest_readings])
    ItemMeasurement.objects.create(stocking=stocking, value=total_value)
