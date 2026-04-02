import json
import logging
from data.models import Meeting
from services import database

logger = logging.getLogger(__name__)
DB = database.DB

def create(title: str, owner: str, date: str):
    logger.info("Creating meeting", extra={"title": title, "date": date})
    try:
        new_meeting = Meeting(title=title, owner=owner, date=date)
        meeting_id = database.create(meeting=new_meeting)
        logger.info("Meeting saved to database")
        return meeting_id
    except Exception as exc:
        logger.error(f"Failed to create meeting: {exc}", exc_info=True)
        raise

def get_all():
    """Get all meetings."""
    logger.info("Fetching all meetings")
    try:
        meetings_data = database.get_all()
        logger.info(f"Found {len(meetings_data)} meetings")
        return meetings_data
    except Exception as exc:
        logger.error(f"Failed to fetch meetings: {exc}", exc_info=True)
        raise

def list():
    """List all meetings to stdout."""
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

def show(meeting_id: str):
    """Show a specific meeting by ID."""
    logger.info(f"Showing meeting {meeting_id}")
    try:
        meeting_data = database.get_by_id(meeting_id)
        if meeting_data:
            print(f"ID: {meeting_data.get('id')}")
            print(f"Title: {meeting_data.get('meeting', {}).get('Title')}")
            print(f"Owner: {meeting_data.get('meeting', {}).get('Owner')}")
            print(f"Date: {meeting_data.get('meeting', {}).get('Date')}")
            action_items = meeting_data.get('meeting', {}).get('ActionItems', [])
            print(f"Action Items: {len(action_items)}")
            if action_items:
                for item in action_items:
                    print(f"  - {item}")
            logger.info(f"Meeting {meeting_id} displayed successfully")
        else:
            logger.warning(f"Meeting {meeting_id} not found")
            print(f"Meeting {meeting_id} not found")
    except Exception as exc:
        logger.error(f"Failed to show meeting: {exc}", exc_info=True)
        raise

def delete(meeting_id: str):
    """Delete a meeting by ID."""
    logger.info(f"Deleting meeting {meeting_id}")
    try:
        if database.delete(meeting_id):
            logger.info(f"Meeting {meeting_id} deleted successfully")
            print(f"Meeting {meeting_id} deleted")
        else:
            logger.warning(f"Meeting {meeting_id} not found for deletion")
            print(f"Meeting {meeting_id} not found")
    except Exception as exc:
        logger.error(f"Failed to delete meeting: {exc}", exc_info=True)
        raise
