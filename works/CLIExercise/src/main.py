#Imports

from typer import Typer
from services import get_currency
from data import models

#Create the Typer cli app
cli = Typer()

#Command to convert ammounts
@cli.command("Convert", help="Convert an amount from one currency to another.")
def convert(amount: str, from_currency: str, to_currency: str):
    #Validate if the amount is a number
    try:
        float(amount)
    except ValueError:
        raise ValueError("Amount must be a valid number.")

    #Validate if the Code lengh have 3 letters 
    if len(from_currency) != 3 or len(to_currency) != 3:
        raise ValueError("Currency codes must be exactly 3 letters.")

    #Call the function to convert 
    get_currency.convert(amount, from_currency.upper(), to_currency.upper())

#Command to List all the currencies and their fields, values
@cli.command("List", help="List all currencies and their current values.")
def list():
    #Call the function to list
    get_currency.list_currencies()

#Command to show the rate from one currency
@cli.command("Rate", help="Get the exchange rate of a specific currency.")
def get_rate(type: str):
    #Call the function
    get_currency.get_rate(type)

#Command to show the historical from one currency
@cli.command("History", help="Show historical exchange rate data")
def history(code: str, base: str , years: int ):
    #Call the function
    get_currency.show_history(code, base, years)


#Runs the CLI
if __name__ == "__main__":
    cli()
