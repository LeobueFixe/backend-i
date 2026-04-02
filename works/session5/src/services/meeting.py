import json
from data.models import Meeting
from services import database

DB = database.DB

def create(title: str, owner: str, date: str):
    new_meeting = Meeting(title = title, owner = owner, date = date)
    database.create(meeting = new_meeting)

def list():
    if not DB.exists():
        return []

    with open(DB, "r") as file:
        content = json.load(file)
    
    for meeting in content:
        print(meeting)
