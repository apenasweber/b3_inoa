from celery import shared_task
from datetime import datetime
from trading.models import Asset
from trading.views import collect_prices
import logging

logger = logging.getLogger(__name__)


@shared_task
def task_collect_prices():
    """
    Executes the task_collect_prices Celery task.
    This task iterates over all assets in the database and calls the collect_prices function
    from the views module for each asset, respecting its check_interval.
    Example Usage:
    ```python
    # Execute the task asynchronously
    task_collect_prices.delay()
    ```
    Inputs: None
    Outputs: None
    """
    logger.info("Iniciando a busca de preços dos ativos...")
    # Get all assets from the database
    assets = Asset.objects.all()

    for asset in assets:
        # Calculate the time since the last price check
        time_since_last_check = (
            datetime.now() - asset.quotations.last().created_at
            if asset.quotations.exists()
            else None
        )

        # If it's time to check the asset's price again, call collect_prices
        if (
            time_since_last_check is None
            or time_since_last_check.total_seconds() // 60 >= asset.check_interval
        ):
            collect_prices(asset.ticker)
            asset.check_and_send_alerts()
            logger.info("Busca de preços concluída.")
