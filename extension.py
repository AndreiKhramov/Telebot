import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(values):

        if len(values) != 3:
            raise ConvertionException('Wrong number of parameters')

        quote, base, amount = values

        if quote == base:
            raise ConvertionException("Can't convert the same currencies")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Can't handle currency {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Can't handle currency {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Can't handle amount {amount}")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        text = json.loads(r.content)[keys[base]]
        text_to_send = f'{amount} {quote} costs {round((text * amount), 3)} {base}s'

        return text_to_send

