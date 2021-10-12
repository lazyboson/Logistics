from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from serviceprovider.models import Provider, Polygon, Coordinate
from serviceprovider.serializers import ProviderSerializer, PolygonSerializer
from serviceprovider.utils import make_return_response, entry_coordinates


# Create your views here.


class ProviderList(APIView):
    """
    List all provider, or create a new snippet.
    """

    def get(self, request):
        """
        :param request:
        :return:
        """
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
           ---
           parameters:
               - name: name
                 description: name of the provider
                 required: true
               - name: email
                 description: email of the provider
                 required: true
               - name: phone_number
                 description: phone number  of the provider
                 required: true
               - name: language
                 description: language  of the provider
                 required: true
               - name: currency
                 description: currency  of the provider
                 required: true
        """
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderDetail(APIView):
    """
    Retrieve, update or delete a provider instance.
    """

    def get_object(self, pk):
        try:
            return Provider.objects.get(pk=pk)
        except Provider.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        ---
        parameters:
            - name: pk
              description: pk of the object to be fetched
              required: true
        """

        provider = self.get_object(pk)
        serializer = ProviderSerializer(provider)
        return Response(serializer.data)

    def put(self, request, pk):
        """
           ---
           parameters:
               - name: pk
                 description: pk of the object to be updated
                 required: true
               - name: name
                 description: name of the provider
                 required: false
               - name: email
                 description: email of the provider
                 required: false
               - name: phone_number
                 description: phone number
                 required: false
               - name: language
                 description: language of provider
                 required: false
               - name: currency
                 description: currency of provider
                 required: false
        """
        provider = self.get_object(pk)
        serializer = ProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
           ---
           parameters:
               - name: pk
                 description: pk of the object to be deleted
                 required: true
        """
        provider = self.get_object(pk)
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PolygonList(APIView):
    """
    List all polygon, or create a new snippet. The returned response is in a format. to make the result in that format a function make_return_response() si created in utils.py
    """

    def get(self, request):
        """
        Get all polygon information in single get call.
        """

        result = Coordinate.objects.select_related('polygon').values('long', 'lat', 'polygon__id', 'polygon__name',
                                                                     'polygon__price', 'polygon__provider__name')
        return Response(make_return_response(result))

    def post(self, request):
        """
        coordinates: each dict has form { "x" : 12, "y" : 12 }. example :  [ { "x" : 1, "y" : 2 }, { "x" : 4, "y": 6 }, { "x" : 1, "y": 8 } ]
        ---
        parameters:
            - name: name
              description: name of the polygon
              required: true
            - name: price
              description: price of polygon
              required: true
            - name: provider
              description: pk of provider
              required: true
            - name: coordinates
              description: a list of dicts.
              required: false

        """
        if not request.data.get('coordinates'):
            return Response(
                "Please Provide Polygon corrdinates in form of an array of two element tuples with x= x-corrdinate, y=y-coordinate",
                status=status.HTTP_400_BAD_REQUEST)
        coordinates = request.data.get('coordinates')
        keys = [u'name', u'price', u'provider']
        data = {key: request.data.get(key) for key in keys}
        serializer = PolygonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            entry_coordinates(serializer.data['id'], coordinates)
            data = {key: serializer.data[key] for key in serializer.data.keys()}
            data['coordinates'] = coordinates
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolygonDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Polygon.objects.get(pk=pk)
        except Polygon.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        ---
        parameters:
            - name: pk
              description: id of polygon object to get
              required: true
        """
        polygon = self.get_object(pk)
        serializer = PolygonSerializer(polygon)
        coordinates = [{'lat': obj.lat, 'long': obj.long} for obj in Coordinate.objects.filter(polygon=pk)]
        data = {key: serializer.data[key] for key in serializer.data.keys()}
        data['coordinates'] = coordinates
        return Response(data)

    def put(self, request, pk):
        """
        coordinates: each dict has form { "x" : 12, "y" : 12 }. example :  [ { "x" : 1, "y" : 2 }, { "x" : 4, "y": 6 }, { "x" : 1, "y": 8 } ]
        ---
        parameters:
            - name: pk
              description: id of polygon object to update
              required: true
            - name: coordinates
              description: a list of dicts.
              required: false
            - name: name
              description: new name of polygon
              required: false
            - name: price
              description: new price of the polygon
              required: false
            - name: provider
              description : new provider id
              required: false

        """
        polygon = self.get_object(pk)
        if request.data.get('coordinates'):
            Coordinate.objects.filter(polygon=pk).delete()
            entry_coordinates(pk, request.data.get('coordinates'))
        serializer = PolygonSerializer(polygon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        ---
        parameters:
            - name: pk
              description: id of polygon object to be deleted
              required: true
        """
        polygon = self.get_object(pk)
        polygon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoordinateList(APIView):
    """
        List all polygon, or create a new snippet.
    """

    def get(self, request):
        polygon = Polygon.objects.all()
        serializer = PolygonSerializer(polygon, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPolygonData(APIView):
    """
     The API to fetch all polygons with  their coordinates matching a given lat, long.
     The returned response is in a particuar format. to make the result in that format a function make_return_response() is created in utils.py
    """

    def post(self, request):
        """
        ---
         parameters:
            - name: lat
              description: latitude
              required: true
            - name: long
              description: longitude
              required: true
        """
        lat = request.data.get('lat')
        long = request.data.get('long')
        result = Coordinate.objects.select_related('polygon').values('long', 'lat', 'polygon__id', 'polygon__name',
                                                                     'polygon__price',
                                                                     'polygon__provider__name').filter(lat=lat,
                                                                                                       long=long)
        return Response(make_return_response(result))
