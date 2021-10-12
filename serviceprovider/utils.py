from rest_framework.response import Response
from rest_framework import status

from serviceprovider.serializers import CoordinateSerializers


def make_return_response(result):
    """
    :param result: a query set
    :return: returns after processing the query set to return the data in a format

    """
    coordinates = {}
    master = {}
    for obj in result:
        if obj['polygon__id'] not in coordinates.keys():
            coordinates[obj['polygon__id']] = [{"lat": obj['lat'], "long": obj['long']}]
        else:
            coordinates[obj['polygon__id']].append({"lat": obj['lat'], "long": obj['long']})

    for obj in result:
        if obj['polygon__id'] not in master.keys():
            master[obj['polygon__id']] = {"polygon_name": obj['polygon__name'], "polygon_price": obj["polygon__price"],
                                          "provider_name": obj["polygon__provider__name"],
                                          "coordinates": coordinates[obj["polygon__id"]]}
    return master


def entry_coordinates(id, coordinates):
    """
    This function makes entries in coordinates table for given polygon_id
    :param id: id of the created polygon object
    :param coordinates:  list of corrdinates [{x:23.56, y:67}, {x:12, y:45}, {x:11, y:76}, {x:10, y:44}]
    :return: None
    """
    data = [{'polygon': id, 'lat': c['x'], 'long': c['y']} for c in coordinates]
    serializer = CoordinateSerializers(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
