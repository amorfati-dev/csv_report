"""URL configuration for upload app."""

from django.urls import path

from . import views

app_name = "upload"

urlpatterns = [
    path("", views.upload_view, name="upload"),
    path("process/", views.process_csv, name="process_csv"),
    path("reports/", views.reports_view, name="reports"),
]
