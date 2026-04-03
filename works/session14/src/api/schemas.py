from pydantic import BaseModel, Field
from typing import Optional, List

class MeetingCreate(BaseModel):
    title: str = Field(min_length=3)
    date: str
    owner: str = Field(min_length=2)
    participants: list[str] = Field(min_items=1)

class MeetingRead(MeetingCreate):
    id: str

class ActionItemCreate(BaseModel):
    description: str = Field(min_length=3)
    owner: str = Field(min_length=2)
    due_date: str

class ActionItemRead(ActionItemCreate):
    id: str

class ActionItemListResponse(BaseModel):
    total: int
    items: list[ActionItemRead]

class MeetingListResponse(BaseModel):
    total: int
    items: list[MeetingRead]

class ErrorResponse(BaseModel):
    error: str
    details: Optional[List[dict]] = None