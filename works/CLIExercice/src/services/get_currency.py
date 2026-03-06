import json
import requests
from pathlib import Path
from typing import List
from data.models import Currency

DB = Path("src/data/currencies.json")


def load_currencies() -> List[Currency]:
    if not DB.exists():
        raise FileNotFoundError(f"Database file not found: {DB}")

    with open(DB, "r") as file:
        data = json.load(file)

    if "currencies" not in data:
        raise ValueError("Invalid database format: missing 'currencies' key")

    return [Currency(**c) for c in data["currencies"]]


def fetch_rates(base: str) -> dict:
    url = f"https://open.er-api.com/v6/latest/{base}"
    response = requests.get(url).json()

    if response.get("result") != "success":
        raise ValueError(f"API error: {response.get('error-type', 'Unknown error')}")

    return response["rates"]

def get_currency_obj(currencies: List[Currency], code: str) -> Currency | None:
    return next((c for c in currencies if c.code == code), None)


def list_currencies(base="USD"):
    currencies = load_currencies()
    rates = fetch_rates(base)

    print(f"\nCurrency values relative to {base}:\n")
    for c in currencies:
        value = rates.get(c.code)
        if value is None:
            print(f"{c.code} - {c.name}: (no data)")
        else:
            print(f"{c.code} - {c.name}: {value:.2f}{c.symbol}")


def convert(amount: str, from_currency: str, to_currency: str):
    currencies = load_currencies()

    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a valid number.")

    rates = fetch_rates(from_currency)

    if to_currency not in rates:
        raise ValueError(
            f"Invalid currency code: {to_currency}. "
            "Use the 'List' command to see available currencies."
        )

    rate = rates[to_currency]
    result = amount * rate

    from_obj = get_currency_obj(currencies, from_currency)
    to_obj = get_currency_obj(currencies, to_currency)

    from_sym = from_obj.symbol if from_obj else ""
    to_sym = to_obj.symbol if to_obj else ""

    print(f"\n{amount}{from_sym} {from_currency} → {to_currency}")
    print(f"Rate: {rate}{to_sym}")
    print(f"Result: {result:.2f}{to_sym}\n")


def get_rate(code: str, base: str = "USD"):
    currencies = load_currencies()
    code = code.upper()

    rates = fetch_rates(base)

    if code not in rates:
        raise ValueError(f"Currency '{code}' not found in API rates.")

    currency = get_currency_obj(currencies, code)
    name = currency.name if currency else "Unknown"
    symbol = currency.symbol if currency else ""

    value = rates[code]

    print(f"\nRate relative to {base}:")
    print(f"{code} - {name}: {value:.2f}{symbol}\n")