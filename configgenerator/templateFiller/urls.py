from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ajax/generate-config/", views.generate_config, name="generate_config")
]