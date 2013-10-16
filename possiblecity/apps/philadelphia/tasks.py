# philadelphia/tasks.py

import os

import json
import requests

from django.conf import settings
from django.contrib.gis.utils import LayerMapping
from models import LotProfile

from celery import task

pwd_parcel_mapping = {
    'opa_code': 'TENCODE', 
    'brt_id': 'BRT_ID',
    'address': 'ADDRESS',
    'pwd_parcel': 'MULTIPOLYGON'
}

def _get_filepath(file):
    return os.path.abspath(os.path.join(settings.PROJECT_ROOT, 'data', file))

@task()
def map():
    data_source = _get_filepath('all_the_rest/pwd_parcels_all_the_rest.shp')
    lm = LayerMapping(LotProfile, data_source, pwd_parcel_mapping,
                      transform=False, encoding='iso-8859-1', unique='TENCODE')
    lm.save(verbose=True, step=1000)


@task()
def check_landuse_vacancy():
    """
    Check landuse data source to get vacancy status. 
    Update database accordingly.
    """
    from apps.lotxlot.models import Lot

    t = datetime.datetime.now() - datetime.timedelta(days=1)
    queryset = queryset_iterator(Lot.objects.filter(created__gt=t))
    for lot in queryset:
        lon = lot.coord.x
        lat = lot.coord.y
        source = settings.PHL_DATA["LAND_USE"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"C_DIG3", "f":"json"}

        data = json.loads(requests.get(source, params=params))

        if data:
            if "features" in data:
                features = data["features"]
                if features[0]:
                    attributes = features[0]["attributes"]
                    if "C_DIG3" in attributes:
                        if attributes["C_DIG3"] == 911:
                            lot.is_vacant = True
                            lot.save(update_fields=["is_vacant",])


@task()
def check_public():
    """
    Check papl assets data source to get public status. 
    Update database accordingly.
    """
    from apps.lotxlot.models import Lot

    t = datetime.datetime.now() - datetime.timedelta(days=1)
    queryset = queryset_iterator(Lot.objects.filter(created__gt=t))
    for lot in queryset:
        lon = lot.coord.x
        lat = lot.coord.y
        source = settings.PHL_DATA["PAPL_ASSETS"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"C_DIG3", "f":"json"}

        data = json.loads(requests.get(source, params=params))

        if data:
            if "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        lot.is_public = True
                        lot.save(update_fields=["is_public",])
                        

@task()    
def get_basereg():
    """
    Check papl parcel data source to get basereg number.
    Update database accordingly.
    """
    from .models import LotProfile

    queryset = queryset_iterator(LotProfile.objects.filter(basereg=''))
    for lot_profile in queryset:
        lon = lot_profile.get_center().x
        lat = lot_profile.get_center().y
        source = settings.PHL_DATA["PAPL_PARCELS"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"BASEREG", "f":"json"}

        data = json.loads(requests.get(source, params=params))

        if data:
            if "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        attributes = features[0]["attributes"]
                        lot_profile.basereg = attributes["BASEREG"]
                        lot_profile.save(update_fields=["basereg",])

