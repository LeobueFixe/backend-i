import os
import json
from pathlib import Path
from data.models import Meeting, MeetingLogs
from uuid import uuid4

DB = Path("src/data/meetings/logs.json")
directory = Path("src/data/meetings")
filename = f"{uuid4()}.md"

def create(meeting:Meeting):
    filepath = os.path.join(directory, filename)

    os.makedirs(directory, exist_ok = True)
    with open(filepath, "w") as file:
        file.writelines(str(meeting))
    
    if not os.path.exists(DB):
        DB.touch()
    
    with open(DB.absolute(), "r") as file:
        breakpoint()
        content = json.loads(file.read())
        print(content)