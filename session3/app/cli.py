import typer
from services.meeting_service import create_meeting, list_meetings

cli = typer.Typer()

@cli.command("create-meeting")
def create_meeting_cmd(title: str, date: str, owner: str) -> None:
    meeting = create_meeting(title, date, owner)
    typer.echo(f"Created: {meeting.id}")

@cli.command("list-meetings")
def list_meetings_cmd() -> None:
    for m in list_meetings():
        typer.echo(f"{m.id} | {m.date} | {m.title}")

if __name__ == "__main__":
    cli()