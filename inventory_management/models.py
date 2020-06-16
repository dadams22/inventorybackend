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


# TODO: make a signals.py file and move these to there
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class InventoryItem(models.Model):
    """ Represents an item in a customer's inventory """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site, related_name='items', on_delete=models.CASCADE)
    last_measurement = models.FloatField(null=True, blank=True)
    last_measurement_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Scale(models.Model):
    """ Represents a scale that can be used for measurements """
    site = models.ForeignKey(Site, related_name='scales', null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(InventoryItem, related_name='scales', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Scale %d' % self.id


class Measurement(models.Model):
    """ Represents a single measurement made by a single scale """
    value = models.FloatField()
    scale = models.ForeignKey(Scale, on_delete=models.PROTECT)
