import logging
from core.validators import validate_iso_date, validate_title, validate_owner
from core.errors import ValidationError
from core.logging_config import configure_logging
import typer
from services import meeting

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

@cli.command("create")
def create(
    title: str = typer.Option(..., "--title", "-t", help="Meeting title"),
    owner: str = typer.Option(..., "--owner", "-o", help="Meeting owner"),
    date: str = typer.Option(..., "--date", "-d", help="Meeting date YYYY-MM-DD"),
):
    logger.info("Creating meeting", extra={"title": title, "date": date})
    try:
        validate_title(title)
        validate_owner(owner)
        validate_iso_date(date)
        meeting.create(title, owner, date)
        typer.echo("Meeting created")
        logger.info("Meeting created successfully")

    except ValidationError as exc:
        logger.warning(f"Validation error: {exc}")
        typer.echo(f"Validation error: {exc}")
        raise typer.Exit(code=get_error_code("ValidationError"))
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=get_error_code("Exception"))

@cli.command()
def list() -> None:
    logger.info("Listing meetings")
    try:
        meeting.list()
        logger.info("Meetings listed successfully")
    except Exception as exc:
        logger.error(f"Error listing meetings: {exc}", exc_info=True)
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=get_error_code("Exception"))

if __name__ == "__main__":
    configure_logging()
    cli()
