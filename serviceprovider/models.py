from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator


class Provider(models.Model):
    """
    A simple model which stores provider basic information
    """
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    language = models.CharField(max_length=20, blank=True)
    currency = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.name


class Polygon(models.Model):
    """
    This model will consider that multiple servicearea can be served by a provider
    """
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name


class Coordinate(models.Model):
    """
    One polygon can have multiple Coordinates at least three as far as definition of polygon as concerned
    so polygon will be foreignkey here
    """

    polygon = models.ForeignKey(Polygon, on_delete=models.CASCADE)
    # assuming standard may be change with database as postgres recommend to use precision 9 scale 7
    long = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
