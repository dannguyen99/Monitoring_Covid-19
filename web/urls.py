from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("vietnam", views.vietNamView, name="vietnam"),
    path("europe", views.euView, name="europe"),
    path("us", views.us_view, name="us"),
    path("test", views.test, name="test")
]
