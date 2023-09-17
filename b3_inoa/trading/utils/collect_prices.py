import logging
import requests
from decouple import Config

logger = logging.getLogger(__name__)


class PriceCollector:
    def __init__(self):
        config = Config(".env")
        self.api_token = config("BRAPI_TOKEN")
        self.api_endpoint = "https://brapi.dev/api/quote"

    def get_asset(self, ticker):
        from trading.models import Asset

        try:
            return Asset.objects.get(ticker=ticker)
        except Asset.DoesNotExist:
            logger.error(f"No asset found for ticker {ticker}")
            return None

    def fetch_price_data(self, ticker):
        try:
            response = requests.get(
                f"{self.api_endpoint}/{ticker}?token={self.api_token}"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching price for asset {ticker}: {e}")
            return None

    def collect_prices(self, ticker):
        asset = self.get_asset(ticker)
        if not asset:
            return f"No asset found for ticker {ticker}"

        data = self.fetch_price_data(asset.ticker)
        if not data:
            return f"Error fetching price data for asset {ticker}"

        if current_price := data["results"][0].get("regularMarketPrice"):
            from trading.models import Quotation

            Quotation.objects.create(asset=asset, price=current_price)
            logger.info(f"Current price of {asset.ticker} is {current_price}")
            return "Collection complete"
        else:
            logger.error(f"No price data for asset {ticker}")
            return f"No price data for asset {ticker}"

    def collect_for_all_assets(self):
        from trading.models import Asset

        for asset in Asset.objects.all():
            self.collect_prices(asset.ticker)


collector = PriceCollector()
collector.collect_for_all_assets()
