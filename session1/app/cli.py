import typer
import datetime
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()

@app.command()
def create_meeting(title: str, day: int, month: int, year: int, owner: str):
    today = datetime.datetime.today()

    try:
        user_date = datetime.datetime(year, month, day)
    except ValueError:
        print("Invalid date!")
        return

    if user_date < today:
        print("Wrong date!")
        return

    table = Table("Title", "Date", "Owner")
    table.add_row(title, user_date.strftime("%Y/%m/%d"), owner)
    console.print(table)

if __name__ == "__main__":
    app()