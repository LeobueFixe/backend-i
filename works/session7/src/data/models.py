from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import Optional

@dataclass
class Meeting:
    title: str
    owner: str
    date: str
    id: Optional[str] = None
    action_items: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __str__(self):
        return (
            "| Field | Value |\n"
            "|-------|--------|\n"
            f"| ID    | {self.id} |\n"
            f"| Title | {self.title} |\n"
            f"| Owner | {self.owner} |\n"
            f"| Date  | {self.date} |\n"
            f"| Actions | {len(self.action_items)} |\n"
            "\n# Meeting\n"
        )

@dataclass
class MeetingLogs:
    meeting: Meeting
    path: str

    def to_dict(self):
        return {
            "id": self.meeting.id,
            "meeting": {
                "Title": self.meeting.title,
                "Owner": self.meeting.owner,
                "Date": self.meeting.date,
                "ActionItems": self.meeting.action_items,
                "CreatedAt": self.meeting.created_at,
            },
            "Path": self.path
        }
    
    def toJson(self):
        return json.dumps(self.to_dict(), indent=2)
