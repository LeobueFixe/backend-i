import os
import json
import logging
from pathlib import Path
from data.models import Meeting, MeetingLogs
from uuid import uuid4

logger = logging.getLogger(__name__)
DB = Path("src/data/meetings/logs.json")
directory = Path("src/data/meetings")

def create(meeting: Meeting):
    logger.info(f"Persisting meeting: {meeting.title}")
    try:
        id = str(uuid4())
        filename = f"{id}.md"
        filepath = directory / filename

        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Created directory: {directory}")
        
        with open(filepath, "w") as file:
            file.write(str(meeting))
        logger.info(f"Meeting file created: {filepath}")

        logs_content = MeetingLogs(meeting, str(filepath)).to_dict()

        if not DB.exists():
            DB.parent.mkdir(parents=True, exist_ok=True)
            DB.write_text("[]")
            logger.debug(f"Created logs database: {DB}")

        with open(DB, "r") as file:
            content = json.load(file)
        content.append(logs_content)

        with open(DB, "w") as file:
            json.dump(content, file, indent=2)
        logger.info(f"Meeting logged in database: {DB}")
    except IOError as exc:
        logger.error(f"IO error persisting meeting: {exc}", exc_info=True)
        raise
    except Exception as exc:
        logger.error(f"Unexpected error persisting meeting: {exc}", exc_info=True)
        raise
    