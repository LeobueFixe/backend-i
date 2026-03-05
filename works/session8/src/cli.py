from typer import Typer
from api.main import api
import uvicorn

cli = Typer(
    name = "FastAPI CLI"
)

@cli.command("Run")
def run():
    uvicorn.run(api)

@cli.command("Request")
def Request():
    ...

if __name__ == "__main__":
    cli()