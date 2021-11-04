from django.urls import path

from core import views

urlpatterns = [
    path("", views.save_event, name="save_event")
]
