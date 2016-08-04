from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404

from api.serializers import DataSerializer
from api.tools import WorldWeatherOnlineReader


import requests

class Data(APIView):

  def get(self, request, format=None):
    
    reader = WorldWeatherOnlineReader(
        request.GET.get('location'),
        request.GET.get('date_from'),
        request.GET.get('date_to'),
        time_interval = '24'
    )

    if reader.hasError():
      message = reader.getError()
      return Response({'error': message})
      
    serializer = DataSerializer(reader.getData())
    data = {
      'data': serializer.getData(),
      'request': request.GET
    }
    return Response(data)

class Temperature(APIView):

  def get(self, request, format=None):
    
    reader = WorldWeatherOnlineReader(
        request.GET.get('location'),
        request.GET.get('date_from'),
        request.GET.get('date_to'),
        time_interval = '24'
    )

    if reader.hasError():
      message = reader.getError()
      return Response({'error': message})
      
    serializer = DataSerializer(reader.getData())
    data = {
      'temperature': serializer.getData()['temperature'],
      'request': request.GET
    }
    return Response(data)


class Humidity(APIView):

  def get(self, request, format=None):
    
    reader = WorldWeatherOnlineReader(
        request.GET.get('location'),
        request.GET.get('date_from'),
        request.GET.get('date_to'),
        time_interval = '24'
    )

    if reader.hasError():
      message = reader.getError()
      return Response({'error': message})
      
    serializer = DataSerializer(reader.getData())
    data = {
      'humidity': serializer.getData()['humidity'],
      'request': request.GET
    }
    return Response(data)