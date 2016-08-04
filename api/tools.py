from datetime import date, datetime, timedelta
import requests

class WorldWeatherOnlineReader:
  """
  World Weather Online (WWO) API allows only period calls up to
  a maximun of 1 month. In order to bypass this limit, a
  WorldWeatherOnlineReader class has been created.
  
  The class splits the user's period into a list of valid
  periods used to make multiple WWO API calls.
  """

  def __init__(self, location, date_from, date_to, **kwargs):
  
    valid = self.validateData(location, date_from, date_to)
    if not valid:
      return
    
    self.query_max_days = kwargs.pop('query_max_days', 30)
    self.time_interval = kwargs.pop('time_interval', '24')
    self.location = location
    self.valid_periods = self.createRequestPeriods()
    self.fetchData()
    
  def validateData(self, location, date_from, date_to):
    if not all([
        self.dateValid(date_from),
        self.dateValid(date_to),
        self.locationValid(location)]):
      return False
    
    self.date_start = self.stringToDate(date_from)
    self.date_end = self.stringToDate(date_to)

    if self.date_start <= date(2008, 07, 01):
      self.error = 'Date must be after 2008-07-01.'
      return False
    return True
  
    
  def locationValid(self, location):
    if location is None:
      self.error = "Please add a location."
      return False
    return True

  def dateValid(self, date):
    if date is None:
      self.error = "Please add date."
      return False
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        self.error = "Invalid date format."
        return False

  def stringToDate(self, date_string):
    """
    Returns date object from string with format yyyy-MM-dd.
    """
    split = [int(i) for i in date_string.split('-')]
    date_object = date(split[0], split[1], split[2])
    return date_object
  
  def dateToString(self, date):
    """
    Returns yyyy-MM-dd from date object.
    """
    return "{0}-{1}-{2}".format(date.year, date.month, date.day)

  def createRequestPeriods(self):
    """
    
    """
    periods = []
    for period in self.generatePeriods(
        self.date_start,
        self.date_end,
        timedelta(days=self.query_max_days)):
      periods.append(period)


    valid_periods = []
    for i in range(len(periods) - 1):
      valid_period = {
        "from": periods[i],
        "to": periods[i+1] - timedelta(days=1)
      }
      valid_periods.append(valid_period)
    return valid_periods


  def generatePeriods(self, beg, end, delta):
    """
    
    """
    curr = beg
    while curr <= end:
      yield curr
      curr += delta
      if curr > end:
        yield end

  def fetchData(self):
    """
    Aggregate WWO API data requests.
    """
    data = []

    for period in self.valid_periods:
      url = (
          'http://api.worldweatheronline.com/' +
          'premium/v1/past-weather.ashx?' +
          'key=3f11b9302a924efbb0b215723160406' +
          '&q=' + self.location +
          '&date=' + self.dateToString(period["from"]) +
          '&enddate=' + self.dateToString(period["to"]) +
          '&tp=' + self.time_interval +
          '&format=json'
      )
    
      req = requests.get(url)
      if not self.isValid(req.json()):
        self.errors = True
        break
      data.append(req.json())
    self.data = data

  def isValid(self, data):
    if u'error' in data[u'data']:
      self.error = data[u'data'][u'error'][0]['msg']
      return False
    return True

  def hasError(self):
    if hasattr(self, 'error'):
      return True
    return False

  def getError(self):
    return self.error

  def getData(self):
    return self.data

        
