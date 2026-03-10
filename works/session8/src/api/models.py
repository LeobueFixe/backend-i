from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class Meeting(BaseModel):
    title: str
    owner: str
    date : datetime
    content: str

    def toMarkdown(self) -> str:
        return (
            "# Meeting\n\n"
            f"**Title:** {self.title}\n\n"
            f"**Owner:** {self.owner}\n\n"
            f"**Date:** {self.date}\n\n"
            "## Content\n"
            f"{self.content}\n"
        )

class MeetingResponse(BaseModel):
    id: UUID

class MeetingRequest(BaseModel):
    title: str
    owner: str
    