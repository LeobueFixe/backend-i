from typer import Typer
from api.main import api
import uvicorn

cli = Typer(
    name = "FastAPI CLI"
)

@cli.command("Run")
def run():
    uvicorn.run(api, host="0.0.0.0")

@cli.command("Request")
def request():
    ...
    
if __name__ == "__main__":
    cli()