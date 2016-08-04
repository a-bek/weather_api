from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/search/$', views.Data.as_view()),
    url(r'^api/search/temperature/$', views.Temperature.as_view()),
    url(r'^api/search/humidity/$', views.Humidity.as_view()),
]
