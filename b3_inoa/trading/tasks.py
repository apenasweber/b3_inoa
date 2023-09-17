import logging
from datetime import datetime
from celery import shared_task
from trading.models import Asset
from trading.views import fetch_asset_by_ticker

logger = logging.getLogger(__name__)

MINUTES_IN_SECOND = 60


@shared_task
def fetch_asset_prices_task():
    """
    Executes the fetch_asset_prices_task Celery task.
    This task fetches prices for assets when it's time to update, based on the asset's check_interval.

    Example Usage:
    ```python
    # Execute the task asynchronously
    fetch_asset_prices_task.delay()
    ```
    """
    _log_and_print("Starting asset price fetch...")

    assets = Asset.objects.all()

    for asset in assets:
        if _is_time_to_update_price(asset):
            _update_asset_price(asset)

    _log_and_print("Asset price fetch completed.")


def _log_and_print(message):
    logger.info(message)
    print(message)


def _is_time_to_update_price(asset):
    time_since_last_check = _get_time_since_last_check(asset)
    return (time_since_last_check is None or
            time_since_last_check.total_seconds() // MINUTES_IN_SECOND >= asset.check_interval)


def _get_time_since_last_check(asset):
    if asset.quotations.exists():
        return datetime.now() - asset.quotations.last().created_at
    return None


def _update_asset_price(asset):
    fetch_asset_by_ticker(asset.ticker)
    asset.check_and_send_alerts()
