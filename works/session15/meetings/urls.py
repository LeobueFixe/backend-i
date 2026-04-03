from django.urls import path
from . import views

urlpatterns = [
    path("", views.meetings_list, name="meetings_list"),
    path("api/", views.meetings_api, name="meetings_api"),
    path("create/", views.create_meeting, name="create_meeting"),
]
