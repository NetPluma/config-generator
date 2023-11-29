from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="Jinja-Templater"),
    path("Excel-Config/", views.generate_from_excel, name="Excel-Config"),
    path("ajax/upload-excel/", views.upload_excel, name="upload_excel"),
    path("ajax/generate-config/", views.generate_config, name="generate_config"),
    path("ajax/generate-multiple-configs/", views.generate_multiple_config, name="generate_multiple_configs")
]