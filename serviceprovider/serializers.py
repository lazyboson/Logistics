from rest_framework import serializers
from serviceprovider.models import Provider, Polygon, Coordinate


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ( 'id', 'name', 'email', 'phone_number', 'language', 'currency')


class PolygonSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = Polygon
        fields = ( 'id', 'provider','name', 'price', )


class CoordinateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Coordinate
        fields = ('id', 'polygon','long', 'lat', )