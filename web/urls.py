from django.urls import path

from . import views

urlpatterns = [
<<<<<<< HEAD
    path("", views.index),
=======
    path("", views.index, name="index"),
    path("vietnam", views.vietNamView, name="vietnam"),
    path("test", views.test, name="test")
>>>>>>> d319f865d427a1a5986da926ddfedeac91b17383
]
