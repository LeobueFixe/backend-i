from dataclasses import dataclass, field
from typing import List

class ActionItem:
    def __init__(self, description: str, owner: str, due_date: str, status: str = "open"):
        self.description = description
        self.owner = owner
        self.due_date = due_date
        self.status = status

@dataclass
class Meeting:
    def __init__(self, id: str, title: str, date: str, owner: str, participants: List[str] = None, action_items: List[ActionItem] = None):
        self.id = id
        self.title = title
        self.date = date
        self.owner = owner
        self.participants = participants if participants is not None else []
        self.action_items = action_items if action_items iss not None else []

class MeetingManager:
    def __init__(self):
        self.meetings: List[Meeting] = []

    def add(self, *meetings: Meeting):
        for meeting in meetings:
            self.meetings.append(meeting)
    
    def list(self) -> List[Meeting]:
        return self.meetings
