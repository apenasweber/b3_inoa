from decouple import Config
from django.core.mail import send_mail

import logging

logger = logging.getLogger(__name__)
config = Config(".env")
API_TOKEN = config("BRAPI_TOKEN")


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
