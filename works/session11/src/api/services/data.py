import json
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from typing import Optional
from ..models import Meeting, MeetingRequest, MeetingResponse, ActionItem
import os

BASE_DIR = Path(__file__).resolve().parent.parent
FOLDER_PATH = BASE_DIR / "data" / "meetings"
DB_PATH = BASE_DIR / "data" / "database.json"


def dbExist():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        DB_PATH.write_text(json.dumps({"meetings": []}, indent=4))


def load():
    dbExist()

    try:
        with open(DB_PATH, "r") as file:
            data = json.load(file)

        if "meetings" not in data:
            data = {"meetings": []}
            save(data)

        return data

    except json.JSONDecodeError:
        data = {"meetings": []}
        save(data)
        return data

def save(data):
    dbExist()

    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=4, default=str)


def listMeetings(title: Optional[str], owner: Optional[str], date: Optional[datetime]):
    db = load()
    meetings = [Meeting(**m) for m in db["meetings"]]

    if title:
        meetings = [m for m in meetings if m.title == title]
    if owner:
        meetings = [m for m in meetings if m.owner == owner]
    if date:
        meetings = [m for m in meetings if datetime.fromisoformat(m.date).date() == date.date()]

    return meetings


def createMeeting(req: MeetingRequest) -> MeetingResponse:
    db = load()
    new_id = str(uuid4())
    FILE_NAME = f"{new_id}.md"
    FILE_PATH = os.path.join(FOLDER_PATH, FILE_NAME)

    meeting = Meeting(
        id=new_id,
        title=req.title,
        owner=req.owner,
        date=req.date,
        content="TODO: summary from model",
        participants=req.participants
    )

    os.makedirs(FOLDER_PATH, exist_ok=True)
    with open(FILE_PATH, "w") as file:
        file.write(meeting.toMarkdown())

    db["meetings"].append(meeting.dict())
    save(db)

    return MeetingResponse(id=new_id)


def getMeeting(meeting_id: str):
    db = load()
    for m in db["meetings"]:
        if m["id"] == meeting_id:
            return Meeting(**m)
    return None


def saveMeeting(meeting: Meeting):
    db = load()
    for idx, m in enumerate(db["meetings"]):
        if m["id"] == meeting.id:
            db["meetings"][idx] = meeting.dict()
            save(db)
            return
    raise ValueError("Meeting not found")


def add_action_item(meeting_id: str, action_item: dict):
    meeting = getMeeting(meeting_id)
    if not meeting:
        return None

    meeting.action_items.append(ActionItem(**action_item))
    saveMeeting(meeting)
    return meeting.action_items[-1]


def list_action_items(meeting_id: str):
    meeting = getMeeting(meeting_id)
    if not meeting:
        return []
    return meeting.action_items


def get_action_item(meeting_id: str, action_item_id: str):
    meeting = getMeeting(meeting_id)
    if not meeting:
        return None
    for item in meeting.action_items:
        if item.id == action_item_id:
            return item
    return None
