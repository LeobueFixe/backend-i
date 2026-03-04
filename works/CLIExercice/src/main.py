from typer import Typer
from services import get_currency
from data import models

cli = Typer()

@cli.command("Convert")
def convert(amount: str, from_currency: str, to_currency: str):
    get_currency.convert(amount, from_currency.upper(), to_currency.upper())

@cli.command("List")
def list():
    get_currency.list_currencies()

@cli.command("Rate")
def get_rate(type: str):
    get_currency.get_rate(type)

if __name__ == "__main__":
    cli()
