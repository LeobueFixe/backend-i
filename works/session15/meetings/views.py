from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from .models import Meeting
import json


@require_http_methods(["GET", "POST"])
def meetings_list(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        date = request.POST.get("date", "").strip()
        owner = request.POST.get("owner", "").strip()

        if not title or not date or not owner:
            return render(
                request,
                "meetings/list.html",
                {
                    "meetings": Meeting.objects.all().order_by("date", "id"),
                    "error": "Title, date, and owner are required.",
                },
            )

        Meeting.objects.create(title=title, date=date, owner=owner)
        return redirect("meetings_list")

    meetings = Meeting.objects.all().order_by("date", "id")
    return render(request, "meetings/list.html", {"meetings": meetings})


@require_http_methods(["GET"])
def meetings_api(request):
    meetings = Meeting.objects.all().order_by("date", "id")
    data = [
        {
            "id": m.id,
            "title": m.title,
            "date": m.date.isoformat(),
            "owner": m.owner,
            "action_items": m.action_items.count(),
        }
        for m in meetings
    ]
    return JsonResponse({"meetings": data}, encoder=DjangoJSONEncoder)


@require_http_methods(["POST"])
def create_meeting(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    title = payload.get("title")
    date = payload.get("date")
    owner = payload.get("owner")

    if not title or not date or not owner:
        return HttpResponseBadRequest("title, date and owner are required")

    meeting = Meeting.objects.create(title=title, date=date, owner=owner)
    return JsonResponse(model_to_dict(meeting), status=201)
