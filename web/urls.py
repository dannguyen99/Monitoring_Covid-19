from django.urls import path

from . import views
from . import apis

urlpatterns = [
    path("", views.index, name="index"),
    path("vietnam", views.vietnam_view, name="vietnam"),
    path("visualization", views.visualization, name="visualization"),
    path("country/<str:geoId>", views.country_view, name="country_view"),
    path("test", views.test, name="test"),
    path("references", views.references, name="references"),
    path("about", views.about, name="about"),
    path("vietnam/api", apis.vietnam_view_api, name='vietnam_api'),
    path("last_update", views.last_update, name="last_update"),
    path("index/api", apis.index_view_api, name='index_api'),
    path("covid19", views.covid19, name='covid19')
]
