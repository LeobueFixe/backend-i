from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class Meeting(BaseModel):
    id: str
    title: str
    owner: str
    date : str
    content: str
    participants: list[str]

    def toMarkdown(self) -> str:
        participants_str = "\n".join(f"- {p}" for p in self.participants)
        return (
            "# Meeting\n\n"
            f"**Title:** {self.title}\n\n"
            f"**Owner:** {self.owner}\n\n"
            f"**Date:** {self.date}\n\n"
            f"**Participants:**\n{participants_str}\n\n"
            "## Content\n"
            f"{self.content}\n"
        )

class MeetingResponse(BaseModel):
    id: UUID

class MeetingRequest(BaseModel):
    title: str
    owner: str
    date: str
    participants: list[str]
    