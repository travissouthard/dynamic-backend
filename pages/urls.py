from django.urls import path

from .views import homeView, aboutView

urlpatterns = [
    path("", homeView, name="home"),
    path("about", aboutView, name="about")
]