from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^$', views.search),
    url(r'^results/$', views.results),
]
