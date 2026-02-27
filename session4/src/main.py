from typer import Typer
from services import meeting


cli = Typer()

@cli.command("create")
def create(title: str, owner: str, date: str):
    meeting.create(title, owner, date)

@cli.command()
def list() -> None:
    ...

if __name__ == "__main__":
    cli()
