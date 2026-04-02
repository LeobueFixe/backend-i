from core.validators import validate_iso_date, validate_title, validate_owner
from core.errors import ValidationError
import typer
from services import meeting

cli = typer.Typer()

@cli.command("create")
def create(
    title: str = typer.Option(..., "--title", "-t", help="Meeting title"),
    owner: str = typer.Option(..., "--owner", "-o", help="Meeting owner"),
    date: str = typer.Option(..., "--date", "-d", help="Meeting date YYYY-MM-DD"),
):
    try:
        validate_title(title)
        validate_owner(owner)
        validate_iso_date(date)
        meeting.create(title, owner, date)
        typer.echo("Meeting created")

    except ValidationError as exc:
        typer.echo(f"Validation error: {exc}")
        raise typer.Exit(code=2)

@cli.command()
def list() -> None:
    meeting.list()

if __name__ == "__main__":
    cli()
