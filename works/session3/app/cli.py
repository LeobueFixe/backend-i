import typer
from services.meeting_service import create_meeting, meetings

cli = typer.Typer()

@cli.command("create-meeting")
def create_meeting_cmd(title: str, date: str, owner: str) -> None:
    meeting = create_meeting(title, date, owner)
    typer.echo(f"Created: {meeting.id}")

@cli.command("list-meetings")
def list_meetings_cmd() -> None:
    for m in meetings.list():
        typer.echo(f"{m.id} | {m.date} | {m.title} | {m.owner} ")

if __name__ == "__main__":
    cli()