from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("vietnam", views.vietnam_view, name="vietnam"),
    path("us", views.us_view, name="us"),
    path("test", views.test, name="test")
]
