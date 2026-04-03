from fastapi import FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
from .models import Meeting, MeetingRequest, MeetingResponse
from .services.data import listMeetings, createMeeting, getMeeting
from .schemas import MeetingCreate, MeetingRead, MeetingListResponse, ErrorResponse
from .routers import action_items

api = FastAPI(
    title="Meeting Note Assistant API",
    version="0.2.0",
    description="Meetings, notes, and action items management",
)
api.include_router(action_items.router)

@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(error="Validation Error", details=exc.errors()).model_dump(),
    )

@api.get("/meetings", response_model=MeetingListResponse)
def list_meetings_route(
    title: Optional[str] = None,
    owner: Optional[str] = None,
    date: Optional[datetime] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    total, items = listMeetings(title, owner, date, limit=limit, offset=offset)
    return {"total": total, "items": items}

@api.post("/meetings", response_model=MeetingRead, status_code=201)
def create_meeting_route(payload: MeetingCreate) -> MeetingRead:
    response = createMeeting(payload)
    return MeetingRead(id=str(response.id), **payload.model_dump())

@api.get("/meetings/{meeting_id}", response_model=Meeting)
def get_meeting_route(meeting_id: str):
    meeting = getMeeting(meeting_id)
    if not meeting:
        raise HTTPException(404, "Meeting not found")
    return meeting


@api.get("/dashboard/summary")
def dashboard_summary():
    total_meetings, meetings = listMeetings(None, None, None, limit=10000, offset=0)
    total_action_items = sum(len(m.action_items) for m in meetings)
    owners = set()
    for m in meetings:
        owners.add(m.owner)
        for ai in m.action_items:
            owners.add(ai.owner)
    
    return {
        "total_meetings": total_meetings,
        "total_action_items": total_action_items,
        "unique_owners": len(owners),
        "owners": sorted(list(owners)),
    }

