from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("vietnam", views.vietnam_view, name="vietnam"),
    path("europe", views.euView, name="europe"),
    path("us", views.us_view, name="us"),
    path("<str:geoId>", views.country_view, name="country_view"),
    path("test", views.test, name="test")
]
