# philadelphia/models.py

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.db.models import Count, Sum

from apps.lotxlot.models import Lot

class Neighborhood(models.Model):
    """
    Information about a Philadelphia neighborhood
    """
    objects = models.GeoManager()

    name = models.CharField(max_length=255)
    map_name = models.CharField(max_length=255)
    list_name = models.CharField(max_length=255)
    bounds = models.MultiPolygonField(srid=4326)

    @property
    def vacant_lot_count(self):
        return Lot.objects.filter(is_vacant=True).filter(coord__within=self.bounds).count()

    @property
    def idea_count(self):
        qs = Lot.objects.filter(
            is_vacant=True).filter(
            coord__within=self.bounds).annotate(
            num_ideas=Count('idea')).aggregate(Sum('num_ideas'))
        return qs["num_ideas__sum"]


    class Meta:
        ordering = ['name']    

    def __unicode__(self):
        return u'%s' % self.map_name

class LotProfile(models.Model):
    """
    City specific information about an individual unit of land in Philadelphia.
    """
    objects = models.GeoManager()

    basereg = models.CharField(max_length=10, blank=True) 
    opa_code = models.CharField( max_length=10, blank=True)
    address = models.CharField(max_length=255, blank=True)
    
    pwd_parcel = models.MultiPolygonField(srid=4326)

    lot = models.OneToOneField(Lot, null=True, blank=True, related_name='profile')
    neighborhood = models.ForeignKey(Neighborhood, null=True, blank=True)

    def get_neighborhood(self):
        try:
            pnt = self.pwd_parcel.point_on_surface
            qs = Neighborhood.objects.filter(bounds__contains=pnt)
            return qs[0]
        except:
            return ''

    def __unicode__(self):
        return u'%s' % self.lot

    def save(self, *args, **kwargs):
        if not self.neighborhood:
            self.neighborhood = self.get_neighborhood()
        super(LotProfile, self).save(*args, **kwargs)

def lot_profile_post_save(sender, **kwargs):
    """
        When a LotProfile instance is created, create a related Lot instance.
        Then use its address data and geometry data to update the related
        Lot address and bounds fields, respectively.
    """
    lot_profile, created = kwargs["instance"], kwargs["created"]
    # if this is a new instance of parcel, 
    # create and populate the related Lot
    if created:
        try:
            coord = lot_profile.pwd_parcel.point_on_surface
        except:
            coord = None
        lot = Lot(address=lot_profile.address.title(),
            bounds=lot_profile.pwd_parcel, 
            coord=coord,
            city='Philadelphia', state='PA', country='US',)
        lot.save()
        lot_profile.lot = lot
        lot_profile.save()

post_save.connect(lot_profile_post_save, sender=LotProfile)

