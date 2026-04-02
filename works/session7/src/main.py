import logging
import json
from core.validators import validate_iso_date, validate_title, validate_owner
from core.errors import ValidationError
from core.logging_config import configure_logging
import typer
from services import meeting, report_service

cli = typer.Typer()
logger = logging.getLogger(__name__)

# Exception to CLI error code mapping
ERROR_CODES = {
    "ValidationError": 2,
    "NotFoundError": 3,
    "PersistenceError": 4,
    "Exception": 1,
}

def get_error_code(exc_type: str) -> int:
    """Map exception type to CLI exit code."""
    return ERROR_CODES.get(exc_type, 1)

@cli.command("create-meeting")
def create(
    title: str = typer.Option(..., "--title", "-t", help="Meeting title"),
    owner: str = typer.Option(..., "--owner", "-o", help="Meeting owner"),
    date: str = typer.Option(..., "--date", "-d", help="Meeting date YYYY-MM-DD"),
):
    """Create a new meeting."""
    logger.info("Creating meeting", extra={"title": title, "date": date})
    try:
        validate_title(title)
        validate_owner(owner)
        validate_iso_date(date)
        meeting_id = meeting.create(title, owner, date)
        typer.echo(f"Meeting created with ID: {meeting_id}")
        logger.info("Meeting created successfully")

    except ValidationError as exc:
        logger.warning(f"Validation error: {exc}")
        typer.echo(f"Validation error: {exc}")
        raise typer.Exit(code=get_error_code("ValidationError"))
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=get_error_code("Exception"))

@cli.command("list-meetings")
def list_meetings() -> None:
    """List all meetings."""
    logger.info("Listing meetings")
    try:
        meeting.list()
        logger.info("Meetings listed successfully")
    except Exception as exc:
        logger.error(f"Error listing meetings: {exc}", exc_info=True)
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=get_error_code("Exception"))

@cli.command("show-meeting")
def show_meeting(
    id: str = typer.Option(..., "--id", "-i", help="Meeting ID"),
) -> None:
    """Show a specific meeting."""
    logger.info(f"Showing meeting {id}")
    try:
        meeting.show(id)
        logger.info("Meeting displayed successfully")
    except Exception as exc:
        logger.error(f"Error showing meeting: {exc}", exc_info=True)
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=get_error_code("Exception"))

@cli.command("delete-meeting")
def delete_meeting(
    id: str = typer.Option(..., "--id", "-i", help="Meeting ID"),
) -> None:
    """Delete a meeting by ID."""
    logger.info(f"Deleting meeting {id}")
    try:
        meeting.delete(id)
        logger.info("Meeting deleted successfully")
    except Exception as exc:
        logger.error(f"Error deleting meeting: {exc}", exc_info=True)
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=get_error_code("Exception"))

@cli.command("report")
def report() -> None:
    """Generate a summary report of all meetings."""
    logger.info("Generating summary report")
    try:
        all_meetings = meeting.get_all()
        summary = report_service.summary(all_meetings)
        typer.echo("=== Meeting Summary ===")
        typer.echo(f"Total Meetings: {summary['meetings']}")
        typer.echo(f"Total Action Items: {summary['action_items']}")
        logger.info("Summary report generated successfully")
    except Exception as exc:
        logger.error(f"Error generating report: {exc}", exc_info=True)
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=get_error_code("Exception"))

@cli.command("period-report")
def period_report(
    from_date: str = typer.Option(..., "--from-date", help="Start date YYYY-MM-DD"),
    to_date: str = typer.Option(..., "--to-date", help="End date YYYY-MM-DD"),
) -> None:
    """Generate a report for meetings within a date range."""
    logger.info(f"Generating period report from {from_date} to {to_date}")
    try:
        validate_iso_date(from_date)
        validate_iso_date(to_date)
        
        report = report_service.period_report(from_date, to_date)
        
        typer.echo("=== Period Report ===")
        typer.echo(f"Period: {report['period']['from']} to {report['period']['to']}")
        typer.echo(f"Total Meetings: {report['meetings']}")
        typer.echo(f"Total Action Items: {report['action_items']}")
        
        if report['details']:
            typer.echo("\nMeetings:")
            for m in report['details']:
                typer.echo(f"  - [{m['id']}] {m['title']} ({m['date']}) - Owner: {m['owner']}, Actions: {m['action_items']}")
        
        logger.info("Period report generated successfully")
    except ValidationError as exc:
        logger.warning(f"Validation error: {exc}")
        typer.echo(f"Validation error: {exc}")
        raise typer.Exit(code=get_error_code("ValidationError"))
    except Exception as exc:
        logger.error(f"Error generating period report: {exc}", exc_info=True)
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=get_error_code("Exception"))

if __name__ == "__main__":
    configure_logging()
    cli()
