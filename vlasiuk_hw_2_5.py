import aiohttp
import asyncio
import json
from datetime import datetime, timedelta


class CurrencyAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    async def fetch_currency(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_data = await response.json()
                if response.status != 200:
                    raise ValueError(f"Failed to fetch data. Status code: {response.status}")
                return response_data

    async def get_currency_for_date(self, date):
        formatted_date = date.strftime("%d.%m.%Y")
        url = f"{self.base_url}&date={formatted_date}"
        return await self.fetch_currency(url)


async def main():
    base_url = "https://api.privatbank.ua/p24api/exchange_rates?json"
    api = CurrencyAPI(base_url)

    current_date = datetime.today().date()

    output_data = []

    for days_ago in range(10):
        target_date = current_date - timedelta(days=days_ago)
        try:
            data = await api.get_currency_for_date(target_date)
            date_str = target_date.strftime('%d.%m.%Y')

            currency_data = {}
            for currency in data['exchangeRate']:
                if currency['currency'] in ['USD', 'EUR']:
                    currency_data[currency['currency']] = {
                        'sale': currency['saleRateNB'],
                        'purchase': currency['purchaseRateNB']
                    }

            output_data.append({date_str: currency_data})
        except Exception as e:
            print(f"Помилка при обробці запиту для дати {target_date}: {e}")

    print(json.dumps(output_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
