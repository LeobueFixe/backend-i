from fastapi import FastAPI, HTTPException
from datetime import datetime
from api.models import Meeting, MeetingRequest, MeetingResponse
from api.services.data import listMeetings, createMeeting, getMeeting

OLLAMA_MODEL = "smollm:135m-base-v0.2-q2_K"
api = FastAPI()


@api.get("/", response_model=list[Meeting])
def list_meetings_route(
    title: str | None = None,
    owner: str | None = None,
    date: datetime | None = None
):
    return listMeetings(title, owner, date)

@api.post("/", response_model=MeetingResponse)
def create_meeting_route(meeting: MeetingRequest):
    return createMeeting(meeting)

@api.get("/{meeting_id}", response_model=Meeting)
def get_meeting_route(meeting_id: str):
    meeting = getMeeting(meeting_id)
    if not meeting:
        raise HTTPException(404, "Meeting not found")
    return meeting
