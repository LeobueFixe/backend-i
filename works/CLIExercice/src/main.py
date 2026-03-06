from typer import Typer
from services import get_currency
from data import models

cli = Typer()

@cli.command("Convert")
def convert(amount: str, from_currency: str, to_currency: str):
    try:
        float(amount)
    except ValueError:
        raise ValueError("Amount must be a valid number.")

    if len(from_currency) != 3 or len(to_currency) != 3:
        raise ValueError("Currency codes must be exactly 3 letters.")

    get_currency.convert(amount, from_currency.upper(), to_currency.upper())

@cli.command("List")
def list():
    get_currency.list_currencies()

@cli.command("Rate")
def get_rate(type: str):
    get_currency.get_rate(type)

if __name__ == "__main__":
    cli()
