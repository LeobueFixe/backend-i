from services.memory_store import meetings
from typer import Typer

cli = Typer()

@cli.command()
def main():
    print(meetings)

if __name__ == "__main__":
    cli()