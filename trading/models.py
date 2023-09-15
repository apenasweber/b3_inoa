from django.db import models
from trading.utils.tickers import TICKER_CHOICES


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

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to add custom business logic before saving the asset object.
        It performs validation to ensure that the price is greater than zero.
        """
        if self.lower_limit >= self.upper_limit:
            raise ValueError("Lower limit must be less than upper limit.")
        if self.check_interval <= 0:
            raise ValueError("Check interval must be greater than zero.")
        super().save(*args, **kwargs)

        # Import the collect_prices function within the method to avoid circular imports
        from trading.utils.collect_prices import collect_prices

        collect_prices(self.ticker)

    def check_price_limits(self) -> str:
        """
        Checks if the asset's current price is outside its price limits and sends an email alert if it is.

        Returns:
            str: A message indicating the success or failure of the check.
        """
        from trading.views import send_email_alert

        last_quotation = self.quotations.last()
        if last_quotation is None:
            return f"No quotations found for asset {self.ticker}"

        current_price = last_quotation.price

        if current_price <= self.lower_limit:
            send_email_alert(self, "Buy")
            return f"Buy alert sent for asset {self.ticker}"

        elif current_price >= self.upper_limit:
            send_email_alert(self, "Sell")
            return f"Sell alert sent for asset {self.ticker}"

        return "Price is within limits"

    def check_and_send_alerts(self):
        """
        Checks the price limits and sends email alerts if necessary.
        """
        self.check_price_limits()
        self.email_sent = True
        self.save()


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

    timestamp = models.DateTimeField(auto_now_add=True)
