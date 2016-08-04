import json
import numpy as np
import datetime

class DataSerializer():

  def __init__(self, data=None):
    self.data_object = data
    self.normalized_data, self.dates = self.normalize(self.data_object)

  def normalize(self, data=None):
    normalized_data = {
      'temp': [],
      'humidity': [],
      'date': [],
      'time': []
    }
    dates = []
    for period in data:
      self.getFields(normalized_data, dates, period)
    return normalized_data, dates

  def getFields(self, normalized_data, dates, data):
    for key, value in data.iteritems():
      if isinstance(value, dict):
        self.getFields(normalized_data, dates, value)
      elif isinstance(value, type([])):
        for obj in value:
          self.getFields(normalized_data, dates, obj)
      else:
        if key == u'tempC':
          normalized_data['temp'].append(float(value))
        if key == 'humidity':
          normalized_data['humidity'].append(float(value))
        if key == 'date':
          normalized_data['date'].append(value)
        if key == 'time':
          normalized_data['time'].append(value)


  def getData(self):
    assert hasattr(self, 'normalized_data'), (
      'No data'
    )
  
    data_values = []
    time_interval = len(self.normalized_data['temp']) / len(self.normalized_data['date'])
    for i in range(len(self.normalized_data['date'])):
      data_values.append({
          'date': self.normalized_data['date'][i / time_interval],
          'temperature': self.normalized_data['temp'][i],
          'humidity': self.normalized_data['humidity'][i],
          'time': self.normalized_data['time'][i]
     })

    data = {
      'temperature' : {
        'min': min(self.normalized_data['temp']),
        'max': max(self.normalized_data['temp']),
        'avg': round(np.mean(self.normalized_data['temp']),1),
        'median': np.median(self.normalized_data['temp'])
      },
      'humidity' : {
        'min': min(self.normalized_data['humidity']),
        'max': max(self.normalized_data['humidity']),
        'avg': round(np.mean(self.normalized_data['humidity']),1),
        'median': np.median(self.normalized_data['humidity'])
      },
      'raw_data' : data_values
    }
    
    return data

  def getTemplateData(self, size=10):

    data = {
      'max_temp': [],
      'min_temp': [],
      'mean_temp': [],
      'max_humidity': [],
      'min_humidity': [],
      'mean_humidity': [],
      'dates': [],
      'temperature' : {
        'min': min(self.normalized_data['temp']),
        'max': max(self.normalized_data['temp']),
        'mean': round(np.mean(self.normalized_data['temp']),1),
        'median': np.median(self.normalized_data['temp'])
      },
      'humidity' : {
        'min': min(self.normalized_data['humidity']),
        'max': max(self.normalized_data['humidity']),
        'mean': round(np.mean(self.normalized_data['humidity']),1),
        'median': np.median(self.normalized_data['humidity'])
      }
    }
    
    length = len(self.normalized_data['date'])
    leap = max(length / size,1)
    
    for i in range(size + 1):
      start = i * leap
      end = (i + 1) * leap
      
      if end > length:
        end = length - 1
        if end == start:
          break
      
      start_date = datetime.datetime.strptime(
          self.normalized_data['date'][start],
          '%Y-%m-%d'
      ).strftime('%b %d,%Y')
      end_date = datetime.datetime.strptime(
          self.normalized_data['date'][end],
          '%Y-%m-%d'
      ).strftime('%b %d,%Y')

      data['dates'].append(start_date + ' - ' + end_date)
      data['max_temp'].append(max(self.normalized_data['temp'][start:end]))
      data['min_temp'].append(min(self.normalized_data['temp'][start:end]))
      data['mean_temp'].append(np.mean(self.normalized_data['temp'][start:end]))
      data['max_humidity'].append(max(self.normalized_data['humidity'][start:end]))
      data['min_humidity'].append(min(self.normalized_data['humidity'][start:end]))
      data['mean_humidity'].append(np.mean(self.normalized_data['humidity'][start:end]))

    return data
    




