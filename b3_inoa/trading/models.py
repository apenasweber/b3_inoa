import logging

from django.db import models
from trading.utils.tickers import TICKER_CHOICES

logger = logging.getLogger(__name__)


CHECK_INTERVAL_CHOICES = [
    (30, "30 minutes"),
    (60, "1 hour"),
    (120, "2 hours"),
    (1440, "1 day"),
]


class Asset(models.Model):
    ticker = models.CharField(choices=TICKER_CHOICES, max_length=10, unique=True)
    lower_limit = models.FloatField(
        help_text="Lower limit: must be less than upper limit. Trigger the email notification when the price is the same or below this limit."
    )
    upper_limit = models.FloatField(
        help_text="Upper limit: must be greater than lower limit."
    )
    check_interval = models.PositiveIntegerField(
        choices=CHECK_INTERVAL_CHOICES,
        help_text="Interval to check the asset's price",
    )
    email = models.EmailField(help_text="Email address to send notifications to.")
    email_sent = models.BooleanField(default=False, verbose_name="Email Sent")

    def __str__(self):
        return self.ticker

    def save(self, check_limits=True, *args, **kwargs):
        """
        Overrides the default save method to add custom business logic before saving the asset object.
        It performs validation to ensure that the price is greater than zero.
        """
        if self.lower_limit >= self.upper_limit:
            raise ValueError("Lower limit must be less than upper limit.")
        if self.check_interval <= 0:
            raise ValueError("Check interval must be greater than zero.")
        super().save(*args, **kwargs)

        if check_limits:
            from trading.utils.collect_prices import PriceCollector

            collector = PriceCollector()
            collector.collect_prices(self.ticker)
            from trading.utils.check_price_limits import check_price_limits

            check_price_limits(self)

    def handle_price_alert(self):
        """
        Checks if the asset's current price is outside its price limits and sends an email alert if it is.
        """
        from trading.utils.check_price_limits import check_price_limits

        result = check_price_limits(self)
        if "alert sent" in result.lower():
            logger.info(f"Email alert sent for asset {self.ticker}")
        else:
            logger.info(f"No email alert required for asset {self.ticker}")

    def check_and_send_alerts(self):
        """
        Checks the price limits and sends email alerts if necessary.
        """
        from trading.utils.check_price_limits import check_price_limits

        self.handle_price_alert()
        self.save(check_limits=False)


class Quotation(models.Model):
    asset = models.ForeignKey(
        "Asset", on_delete=models.CASCADE, related_name="quotations"
    )
    price = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["price"]
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"

    def __str__(self) -> str:
        """
        Returns a string representation of the quotation.
        """
        return f"{self.asset} - Price: {self.price}"

    def save(self, *args, **kwargs) -> None:
        """
        Performs custom business logic and validation before saving the quotation.
        """
        if self.price <= 0:
            raise ValueError("Price must be greater than zero")

        super().save(*args, **kwargs)

        return f"Quotation for {self.asset} - Price: {self.price}"
