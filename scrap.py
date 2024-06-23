import requests

from assets import COINGECKO_IDS, TYPES


def current_cryptocurrency_prices(tickets: list[str], currencies: list[str]):
    COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
    try:
        data = requests.get(
            COINGECKO_API_URL,
            {
                "ids": ",".join(COINGECKO_IDS[ticket] for ticket in tickets),
                "vs_currencies": ",".join(currencies),
            },
        ).json()
    except requests.exceptions.RequestException as e:
        raise e

    return {
        ticket: {
            currency.upper(): data[COINGECKO_IDS[ticket]][currency]
            for currency in data[COINGECKO_IDS[ticket]]
        }
        for ticket in tickets
    }


def current_currency_prices(tickets: list[str], currencies: list[str]):
    URL = "https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off"
    prices = {}
    for currency in currencies:
        if currency == "RUB":
            data = requests.get(URL).json()["cbrf"]["data"][0][3]
            prices["RUB"] = {"RUB": 1, "USD": 1 / data}
        elif currency == "USD":
            data = requests.get(URL).json()["cbrf"]["data"][0][3]
            prices["USD"] = {"RUB": data, "USD": 1}
    return prices


def current_prices(tickets: list[str], currencies: list[str]):
    cryptocurrency = []
    currency = []
    for ticket in tickets:
        match TYPES[ticket]:
            case "cryptocurrency":
                cryptocurrency.append(ticket)
            case "currency":
                currency.append(ticket)
    r = current_cryptocurrency_prices(
        cryptocurrency, currencies
    ) | current_currency_prices(currency, currencies)
    return r
