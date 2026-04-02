import json
import logging
from data.models import Meeting
from services import database

logger = logging.getLogger(__name__)
DB = database.DB

def create(title: str, owner: str, date: str):
    logger.info("Creating meeting", extra={"title": title, "date": date})
    try:
        new_meeting = Meeting(title = title, owner = owner, date = date)
        database.create(meeting = new_meeting)
        logger.info("Meeting saved to database")
    except Exception as exc:
        logger.error(f"Failed to create meeting: {exc}", exc_info=True)
        raise

def list():
    logger.info("Fetching all meetings")
    try:
        if not DB.exists():
            logger.info("No meetings database found")
            return []

        with open(DB, "r") as file:
            content = json.load(file)
        
        logger.info(f"Found {len(content)} meetings")
        for meeting in content:
            print(meeting)
    except Exception as exc:
        logger.error(f"Failed to list meetings: {exc}", exc_info=True)
        raise
