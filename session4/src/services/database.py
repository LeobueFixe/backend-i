from data.models import Meeting
import os
from uuid import uuid4


def create(meeting:Meeting):
    directory = "src/data/meetings"
    filename = f"{uuid4()}.md"
    filepath = os.path.join(directory, filename)

    os.makedirs(directory, exist_ok=True)
    with open(filepath, "w") as file:
        file.writelines(str(meeting))