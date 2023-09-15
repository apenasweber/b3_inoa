import requests
from decouple import Config
from django.core.mail import send_mail

from trading.models import Asset, Quotation
import logging

logger = logging.getLogger(__name__)
config = Config(".env")

API_TOKEN = config("BRAPI_TOKEN")


def collect_prices(ticker):
    """
    Collects the prices of a specific asset by making API requests and stores them in the Quotation model.

    Args:
        ticker (str): The ticker of the asset to collect prices for.

    Returns:
        str: A message indicating the success or failure of the collection.
    """
    try:
        asset = Asset.objects.get(ticker=ticker)
    except Asset.DoesNotExist:
        return f"No asset found for ticker {ticker}"

    try:
        response = requests.get(
            f"https://brapi.dev/api/quote/{asset.ticker}?token={API_TOKEN}"
        )
        response.raise_for_status()
        data = response.json()
        current_price = data["results"][0].get("regularMarketPrice", None)
        logging.info(f"Current price of {asset.ticker} is {current_price}")
        if current_price is not None:
            Quotation.objects.create(asset=asset, price=current_price)
        else:
            return f"No price data for asset {asset.ticker}"

    except requests.RequestException as e:
        return f"Error fetching price for asset {asset.ticker}: {e}"

    return "Collection complete"


def send_email_alert(asset, action):
    """
    Sends an email alert to an investor.

    Args:
        asset (Asset): Represents an asset from the Asset model.
        action (str): Represents an action (e.g., "Buy" or "Sell").

    Returns:
        None

    Raises:
        Any errors that occur during the email sending process will be raised as exceptions.

    Example Usage:

        send_email_alert(asset, action)

    """
    recipient_email = asset.email
    logger.info(f"Tentando enviar e-mail para {asset.email} sobre a ação {action}...")
    send_mail(
        f"Alert for {action} on {asset.ticker}",
        f"The price of the asset {asset.ticker} suggests a {action}",
        asset.email,
        [recipient_email],
        fail_silently=False,
    )

    logger.info(f"E-mail enviado com sucesso para {asset.email}.")
