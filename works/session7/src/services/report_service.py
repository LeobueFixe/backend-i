import logging
from datetime import datetime
from services import meeting

logger = logging.getLogger(__name__)


def summary(meetings: list[dict]) -> dict:
    """Generate a summary report of meetings and action items."""
    logger.info("Generating summary report")
    try:
        total_meetings = len(meetings)
        total_action_items = sum(
            len(m.get("meeting", {}).get("ActionItems", []))
            for m in meetings
        )
        result = {
            "meetings": total_meetings,
            "action_items": total_action_items,
        }
        logger.info(f"Summary: {total_meetings} meetings, {total_action_items} action items")
        return result
    except Exception as exc:
        logger.error(f"Error generating summary: {exc}", exc_info=True)
        raise


def period_report(from_date: str, to_date: str) -> dict:
    """Generate a report for meetings within a date range."""
    logger.info(f"Generating period report from {from_date} to {to_date}")
    try:
        # Parse dates
        from_datetime = datetime.strptime(from_date, "%Y-%m-%d")
        to_datetime = datetime.strptime(to_date, "%Y-%m-%d")
        
        # Get all meetings
        all_meetings = meeting.get_all()
        
        # Filter meetings within date range
        filtered_meetings = []
        for m in all_meetings:
            meeting_date = m.get("meeting", {}).get("Date")
            if meeting_date:
                try:
                    m_datetime = datetime.strptime(meeting_date, "%Y-%m-%d")
                    if from_datetime <= m_datetime <= to_datetime:
                        filtered_meetings.append(m)
                except ValueError:
                    logger.warning(f"Invalid date format: {meeting_date}")
                    continue
        
        # Generate summary for filtered meetings
        total_meetings = len(filtered_meetings)
        total_action_items = sum(
            len(m.get("meeting", {}).get("ActionItems", []))
            for m in filtered_meetings
        )
        
        result = {
            "period": {
                "from": from_date,
                "to": to_date,
            },
            "meetings": total_meetings,
            "action_items": total_action_items,
            "details": [
                {
                    "id": m.get("id"),
                    "title": m.get("meeting", {}).get("Title"),
                    "date": m.get("meeting", {}).get("Date"),
                    "owner": m.get("meeting", {}).get("Owner"),
                    "action_items": len(m.get("meeting", {}).get("ActionItems", [])),
                }
                for m in filtered_meetings
            ]
        }
        logger.info(f"Period report: {total_meetings} meetings, {total_action_items} action items")
        return result
    except ValueError as exc:
        logger.error(f"Invalid date format: {exc}")
        raise
    except Exception as exc:
        logger.error(f"Error generating period report: {exc}", exc_info=True)
        raise
