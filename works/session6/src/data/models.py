from dataclasses import dataclass
import json

@dataclass
class Meeting:
    title: str
    owner: str
    date: str

    def __str__(self):
        return (
            "| Field | Value |\n"
            "|-------|--------|\n"
            f"| Title | {self.title} |\n"
            f"| Owner | {self.owner} |\n"
            f"| Date  | {self.date} |\n"
            "\n# Meeting\n"
        )

@dataclass
class MeetingLogs:
    meeting: Meeting
    path: str

    def to_dict(self):
        return {
            "meeting": {
                "Title": self.meeting.title,
                "Owner": self.meeting.owner,
                "Date": self.meeting.date,
            },
            "Path": self.path
        }
    
    def toJson(self):
        return json.dumps(self.to_dict(), indent=2)
