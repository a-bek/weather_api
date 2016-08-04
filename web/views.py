from django.shortcuts import render
from django.http import HttpResponseRedirect

from api.tools import WorldWeatherOnlineReader
from api.serializers import DataSerializer

from web.forms import LocationForm, DateFromForm, DateToForm

from django.contrib import messages 


def search(request):
  # if this is a POST request we need to process the form data

  if request.method == 'GET':
    location = LocationForm()
    date_from = DateFromForm()
    date_to = DateToForm()
    return render(
      request,
      'search.html',
      {
        'location': location,
        'date_from': date_from,
        'date_to': date_to
      }
    )


def results(request):

  if request.method == 'GET':

    location = LocationForm(request.GET)
    date_from = DateFromForm(request.GET)
    date_to = DateToForm(request.GET)
    
    
    if not all([location.is_valid(), date_from.is_valid(), date_to.is_valid()]):
      return render(
        request,
        'search.html',
        {
          'location': location,
          'date_from': date_from,
          'date_to': date_to
        }
      )
      
      
    reader = WorldWeatherOnlineReader(
        request.GET.get("location"),
        request.GET.get("date_from"),
        request.GET.get("date_to"),
        time_interval='24'
    )

    if reader.hasError():
      message = reader.getError()
      return render(
        request,
        'search.html',
        {
          'location': location,
          'date_from': date_from,
          'date_to': date_to,
          'error': message
        }
      )

    serializer = DataSerializer(reader.getData())
    data = serializer.getTemplateData(size=10)

    return render(
      request,
      'visuals.html',
      {
        'max_temp_array': data['max_temp'],
        'min_temp_array': data['min_temp'],
        'mean_temp_array': data['mean_temp'],
        'max_humidity_array': data['max_humidity'],
        'min_humidity_array': data['min_humidity'],
        'mean_humidity_array': data['mean_humidity'],
        'max_temp': data['temperature']['max'],
        'min_temp': data['temperature']['min'],
        'mean_temp': data['temperature']['mean'],
        'max_humidity': data['humidity']['max'],
        'min_humidity': data['humidity']['min'],
        'mean_humidity': data['humidity']['mean'],
        'dates': data['dates'],
        'location': location,
        'date_from': date_from,
        'date_to': date_to
      }
    )
