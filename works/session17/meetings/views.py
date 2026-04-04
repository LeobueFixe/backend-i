from django.shortcuts import render
from .models import Meeting


def meetings_list(request):
    meetings = Meeting.objects.all().order_by("date", "id")
    return render(request, "meetings/list.html", {"meetings": meetings})
