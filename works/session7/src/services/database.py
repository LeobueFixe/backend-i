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
        meeting.id = id
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
        return id
    except IOError as exc:
        logger.error(f"IO error persisting meeting: {exc}", exc_info=True)
        raise
    except Exception as exc:
        logger.error(f"Unexpected error persisting meeting: {exc}", exc_info=True)
        raise

def get_all() -> list[dict]:
    """Return all meetings from database."""
    logger.info("Reading all meetings from database")
    try:
        if not DB.exists():
            logger.info("Database does not exist")
            return []
        
        with open(DB, "r") as file:
            content = json.load(file)
        logger.info(f"Retrieved {len(content)} meetings")
        return content
    except Exception as exc:
        logger.error(f"Error reading database: {exc}", exc_info=True)
        raise

def get_by_id(meeting_id: str) -> dict:
    """Get a specific meeting by ID."""
    logger.info(f"Reading meeting {meeting_id} from database")
    try:
        all_meetings = get_all()
        for meeting in all_meetings:
            if meeting.get("id") == meeting_id:
                logger.info(f"Found meeting {meeting_id}")
                return meeting
        logger.warning(f"Meeting {meeting_id} not found")
        return None
    except Exception as exc:
        logger.error(f"Error reading meeting {meeting_id}: {exc}", exc_info=True)
        raise

def delete(meeting_id: str) -> bool:
    """Delete a meeting by ID."""
    logger.info(f"Deleting meeting {meeting_id}")
    try:
        all_meetings = get_all()
        updated_meetings = [m for m in all_meetings if m.get("id") != meeting_id]
        
        if len(all_meetings) == len(updated_meetings):
            logger.warning(f"Meeting {meeting_id} not found")
            return False
        
        with open(DB, "w") as file:
            json.dump(updated_meetings, file, indent=2)
        logger.info(f"Meeting {meeting_id} deleted successfully")
        
        # Also delete the markdown file
        all_meetings = get_all()
        for m in all_meetings:
            if m.get("id") == meeting_id:
                path = m.get("Path")
                if path and Path(path).exists():
                    Path(path).unlink()
                    logger.info(f"Deleted meeting file: {path}")
                break
        
        return True
    except Exception as exc:
        logger.error(f"Error deleting meeting {meeting_id}: {exc}", exc_info=True)
        raise
    