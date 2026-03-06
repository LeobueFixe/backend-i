import os
import json
from pathlib import Path
from data.models import Meeting, MeetingLogs
from uuid import uuid4

DB = Path("src/data/meetings/logs.json")
directory = Path("src/data/meetings")

def create(meeting: Meeting):
    id = str(uuid4())
    filename = f"{id}.md"
    filepath = directory / filename

    os.makedirs(directory, exist_ok=True)
    with open(filepath, "w") as file:
        file.write(str(meeting))

    logs_content = MeetingLogs(meeting, str(filepath)).to_dict()

    if not DB.exists():
        DB.parent.mkdir(parents=True, exist_ok=True)
        DB.write_text("[]")

    with open(DB, "r") as file:
        content = json.load(file)
    content.append(logs_content)

    with open(DB, "w") as file:
        json.dump(content, file, indent=2)
    