# Currency Converter CLI

## Overview
This command‑line application provides quick access to real‑time currency information directly from the terminal. It loads a local database of currency metadata (names and symbols) and retrieves live exchange rates from an external API. The tool is designed to solve three common problems:

- Converting an amount from one currency to another using up‑to‑date exchange rates.
- Checking the current exchange rate of a specific currency relative to a base currency.
- Listing all supported currencies stored in the local database.

The application is useful for developers, students, travelers, or anyone who needs fast currency information without opening a browser.

---

## Installation

The project uses a requirements.txt file for dependency management. The recommended installation method is uv, but pip works as well.

### 1. Clone the repository
```bash
git clone <https://github.com/LeobueFixe/backend-i.git>
cd <cd works/CLIExercise/src>
```

### 2. Create and activate a virtual environment
Using uv (recommended)
```bash
uv venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
````
Using Python directly
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
Using uv
```bash
uv pip install -r requirements.txt
```

Using pip
```bash
pip install -r requirements.txt
```

### Usage
Run the CLI using:
```bash
python main.py <command> [arguments]
```
To see the available commands, simply use
```bash
python main.py --help
```

Convert an amount
```bash
python main.py Convert {Value} {From} {To}
```

List all supported currencies
```bash
python main.py List
```

Get the exchange rate of a specific currency
```bash
python main.py Rate {Code}
```

Plots a historical exchange rate chart in the terminal
```bash
History {Compare} {Base} {Years}
```

Examples
```bash
python main.py Convert 100 eur usd
python main.py List
python main.py Rate EUR
python main.py History Eur usd 10
```
## Commands Overview

| Command | Description |
|--------|-------------|
| `Convert <amount> <from> <to>` | Converts an amount between two currencies. |
| `List` | Displays all supported currencies and their current values relative to USD. |
| `Rate <code>` | Shows the exchange rate of a specific currency relative to USD. |
| `History <code> <base> <years>` | Shows the exchange rate of a specific currency relative to USD. |