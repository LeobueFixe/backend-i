from fastapi import APIRouter, HTTPException
from uuid import uuid4
from ..schemas import ActionItemCreate, ActionItemRead
from ..services.data import add_action_item, list_action_items, get_action_item

router = APIRouter(prefix="/meetings", tags=["action-items"])

@router.post("/{meeting_id}/action-items", response_model=ActionItemRead, status_code=201)
def create_action_item(meeting_id: str, payload: ActionItemCreate):
    # note: payload validation is mostly handled by Pydantic schema
    if not payload.due_date:
        raise HTTPException(400, "Due date is required")

    item_id = str(uuid4())
    item_data = {"id": item_id, **payload.model_dump()}
    created = add_action_item(meeting_id, item_data)

    if created is None:
        raise HTTPException(404, "Meeting not found")

    return created

@router.get("/{meeting_id}/action-items", response_model=list[ActionItemRead])
def list_action_items_route(meeting_id: str):
    return list_action_items(meeting_id)

@router.get("/{meeting_id}/action-items/{action_item_id}", response_model=ActionItemRead)
def get_action_item_route(meeting_id: str, action_item_id: str):
    item = get_action_item(meeting_id, action_item_id)
    if item is None:
        raise HTTPException(404, "Action item not found")
    return item
