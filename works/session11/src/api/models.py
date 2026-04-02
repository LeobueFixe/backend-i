from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class ActionItem(BaseModel):
    id: str
    description: str
    owner: str
    due_date: str

class Meeting(BaseModel):
    id: str
    title: str
    owner: str
    date : str
    content: str
    participants: list[str]
    action_items: list[ActionItem] = []

    def toMarkdown(self) -> str:
        participants_str = "\n".join(f"- {p}" for p in self.participants)
        action_items_str = "\n".join(f"- [{ai.id}] {ai.description} (owner:{ai.owner} due:{ai.due_date})" for ai in self.action_items)
        return (
            "# Meeting\n\n"
            f"**Title:** {self.title}\n\n"
            f"**Owner:** {self.owner}\n\n"
            f"**Date:** {self.date}\n\n"
            f"**Participants:**\n{participants_str}\n\n"
            f"**Action Items:**\n{action_items_str if action_items_str else 'None'}\n\n"
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
    