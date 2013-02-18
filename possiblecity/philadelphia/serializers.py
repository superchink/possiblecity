# philadelphia/serializers.py
from django.forms import widgets

from rest_framework import serializers

from possiblecity.rest_framework_gis.fields import GeometryField
from possiblecity.rest_framework_gis.serializers import GeoModelSerializer
from .models import Lot

class LotModelSerializer(GeoModelSerializer):
    class Meta:
        model = Lot
        fields = ('id', 'address', 'coord')

class LotSerializer(serializers.Serializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    address = serializers.CharField(required=False,
                                  max_length=100)
    coord = GeometryField()

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance.
        """
        if instance:
            # Update existing instance
            instance.address = attrs.get('coord', instance.address)
            instance.coord = attrs.get('code', instance.coord)

            return instance

        # Create new instance
        return Lot(**attrs)