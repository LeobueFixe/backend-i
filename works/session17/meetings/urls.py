from django.urls import path
from . import views

urlpatterns = [
    path("", views.meetings_list, name="meetings_list"),
]
