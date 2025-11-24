# FlexRate: A Simple Currency Converter

FlexRate is a small Python application that converts amounts between currencies based on user input. It supports both static exchange rates (useful for testing or offline use) and an optional live rate provider that can be wired to a public exchange rate API.

## Features

- Convert from one currency to another (e.g. GBP to EUR)
- Support for common currencies: GBP, EUR, USD, JPY, AUD (easily extendable)
- Static rate provider for predictable results
- Pluggable design for live API based rates
- Command line usage with simple prompts
- Basic input validation and error handling

## Requirements

- Python 3.9 or later (3.10+ recommended)
- `requests` (for live API provider, optional)
- `pytest` (for tests)

## Installation

1. Clone or download the repository:

git clone [https://github.com/Morgan-Jo/Number-Converter-Fun/Flexrate.git](https://github.com/Morgan-Jo/Number-Converter-Fun/tree/main/Flexrate)]
cd flexrate

2. Install dependencies:

```bash
pip install -r requirements.txt
