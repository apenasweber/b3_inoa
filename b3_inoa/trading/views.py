import logging
import requests
from decouple import Config
from django.core.mail import send_mail

logger = logging.getLogger(__name__)
config = Config(".env")
API_TOKEN = config("BRAPI_TOKEN")
BRAPI_URL_TEMPLATE = "https://brapi.dev/api/quote/{}?token={}"


def fetch_asset_by_ticker(ticker):
    from trading.models import Asset

    try:
        return Asset.objects.get(ticker=ticker)
    except Asset.DoesNotExist:
        return None


def get_asset_price_from_api(ticker):
    url = BRAPI_URL_TEMPLATE.format(ticker, API_TOKEN)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["results"][0].get("regularMarketPrice", None)


def store_quotation_for_asset(asset, price):
    from trading.models import Quotation

    Quotation.objects.create(asset=asset, price=price)


def collect_asset_prices(ticker):
    asset = fetch_asset_by_ticker(ticker)
    if not asset:
        return f"No asset found for ticker {ticker}"

    try:
        current_price = get_asset_price_from_api(asset.ticker)
        if current_price is None:
            return f"No price data for asset {asset.ticker}"

        store_quotation_for_asset(asset, current_price)
        logger.info(f"Current price of {asset.ticker} is {current_price}")
    except requests.RequestException as e:
        return f"Error fetching price for asset {asset.ticker}: {e}"

    return "Collection complete"


def send_price_alert_email(asset, action):
    recipient_email = asset.email
    subject = f"Alert for {action} on {asset.ticker}"
    message = f"The price of the asset {asset.ticker} suggests a {action}"

    try:
        send_mail(subject, message, asset.email, [recipient_email], fail_silently=False)
        asset.email_sent = True
        asset.save()
        logger.info(f"Email sent to: {asset.email}.")
    except Exception as error:
        asset.email_sent = False
        logger.error(f"Error sending email to {asset.email}: {error}")
        return f"We had a problem sending email to {asset.email} from your email configuration"
