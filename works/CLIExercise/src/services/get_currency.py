#Imports

import json
import requests
import plotext
import os
from pathlib import Path
from typing import List
from data.models import Currency
from datetime import datetime, timedelta

#Path to my DB in Json
DB = Path("data/currencies.json")

#This function loads DB file
def load_currencies() -> List[Currency]:
    
    #Verify that the file exists, if not raise an Error
    if not DB.exists():
        raise FileNotFoundError(f"Database file not found: {DB}")
    
    #Open and read the file
    with open(DB, "r") as file:
        data = json.load(file)

    #Validate the structure
    if "currencies" not in data:
        raise ValueError("Invalid database format: missing 'currencies' key")

    #Convert dictionarys into objects
    return [Currency(**c) for c in data["currencies"]]

#Function responsible for retrieving the value of each currency in real time
def fetch_rates(base: str) -> dict:
    #Builds the API URL based on the currency the user chooses, or USD because that's the default.
    #Then send a Get request and parse Json response
    url = f"https://open.er-api.com/v6/latest/{base}"
    response = requests.get(url).json()

    #Validate if the API returned a successful result
    if response.get("result") != "success":
        raise ValueError(f"API error: {response.get('error-type', 'Unknown error')}")

    #Return the dictionary conataining currencies rates
    return response["rates"]

#Function responsible for find a currency by code
def get_currency_obj(currencies: List[Currency], code: str) -> Currency | None:
    return next((c for c in currencies if c.code == code), None)

#List all currencies
def list_currencies(base="USD"):
    #Loads Json file with all currencies and their fields
    currencies = load_currencies()
    #Loads the values, comparing them with the database chosen by the user
    rates = fetch_rates(base)

    print(f"\nCurrency values relative to {base}:\n")

    #Loop responsible for print all currencies and their fields, values
    for c in currencies:
        value = rates.get(c.code)
        if value is None:
            print(f"{c.code} - {c.name}: (no data)")
        else:
            print(f"{c.code} - {c.name}: {value:.2f}{c.symbol}")


#Function to convert from one currency to other
def convert(amount: str, from_currency: str, to_currency: str):
    currencies = load_currencies()

    #Validate and convert the amount to float type
    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a valid number.")

    #Fetch exchange rates using the source currency as the base
    rates = fetch_rates(from_currency)

    #Validate if the currency exists in the API Response
    if to_currency not in rates:
        raise ValueError(
            f"Invalid currency code: {to_currency}. "
            "Use the 'List' command to see available currencies."
        )

    #Get the conversion rate and calculate
    rate = rates[to_currency]
    result = amount * rate

    #Retrieve currency objects to access symbols
    from_obj = get_currency_obj(currencies, from_currency)
    to_obj = get_currency_obj(currencies, to_currency)
    from_sym = from_obj.symbol if from_obj else ""
    to_sym = to_obj.symbol if to_obj else ""

    #Print the conversion summary
    print(f"\n{amount}{from_sym} {from_currency} → {to_currency}")
    print(f"Rate: {rate}{to_sym}")
    print(f"Result: {result:.2f}{to_sym}\n")

#Get the rate by code
def get_rate(code: str, base: str = "USD"):
    currencies = load_currencies()
    #Turn the code to uppercase
    code = code.upper()

    #Get the rate
    rates = fetch_rates(base)

    #Validate if the code is in the API response
    if code not in rates:
        raise ValueError(f"Currency '{code}' not found in API rates.")

    #Get the name and symbol from Json file
    currency = get_currency_obj(currencies, code)
    name = currency.name if currency else "Unknown"
    symbol = currency.symbol if currency else ""

    #Extract the rate value
    value = rates[code]

    print(f"\nRate relative to {base}:")
    print(f"{code} - {name}: {value:.2f}{symbol}\n")

#Show historical exchange rates using the Frankfurter API
def show_history(code: str, base: str = "USD", years: int = 1):
    code = code.upper()
    base = base.upper()

    #Calculate date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365 * years)

    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")

    #Free API (no key needed)
    url = f"https://api.frankfurter.app/{start}..{end}?from={base}&to={code}"

    #Fetch raw response
    response_text = requests.get(url).text

    #Parse JSON safely
    try:
        response = json.loads(response_text)
    except json.JSONDecodeError:
        raise ValueError(f"API did not return JSON:\n{response_text}")

    if "rates" not in response:
        raise ValueError(f"Failed to fetch historical data: {response}")

    rates = response["rates"]

    #Convert dates for plotext
    def format_date(d):
        return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")

    dates = [format_date(d) for d in rates.keys()]
    values = [rates[d][code] for d in rates.keys()]

    #Clear previous plot
    try:
        plotext.clear_plot()
    except:
        plotext.clear_data()

    #Draw chart
    plotext.plot(dates, values)
    plotext.title(f"{code}/{base} over {years} year(s)")
    plotext.xlabel("Date")
    plotext.ylabel("Rate")
    plotext.show()
