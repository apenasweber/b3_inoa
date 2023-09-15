from django.contrib import admin
from trading.models import Asset, Quotation


def check_and_send_alerts(modeladmin, request, queryset):
    for asset in queryset:
        asset.check_and_send_alerts()


check_and_send_alerts.short_description = "Check and Send Alerts for Selected Assets"


class QuotationInline(admin.TabularInline):
    model = Quotation
    fields = ("price", "timestamp")
    readonly_fields = ("price", "timestamp")
    extra = 0  # Number of empty forms to display


class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "ticker",
        "last_price",
        "last_price_timestamp",
        "email_sent",
        "lower_limit",
        "upper_limit",
        "check_interval",
        "email",
    )

    actions = [check_and_send_alerts]
    search_fields = ("ticker",)
    list_filter = ("check_interval",)
    fields = ("ticker", "lower_limit", "upper_limit", "check_interval", "email")
    inlines = [QuotationInline]

    def last_price(self, obj):
        latest_quotation = obj.quotations.last()
        return latest_quotation.price if latest_quotation else "No price available"

    last_price.short_description = "Last Price"

    def last_price_timestamp(self, obj):
        latest_quotation = obj.quotations.last()
        return (
            latest_quotation.timestamp if latest_quotation else "No timestamp available"
        )

    last_price_timestamp.short_description = "Last Price Timestamp"


class QuotationAdmin(admin.ModelAdmin):
    list_display = ("asset", "price", "timestamp")
    search_fields = ("asset__ticker",)
    list_filter = ("timestamp",)


admin.site.register(Asset, AssetAdmin)
admin.site.register(Quotation, QuotationAdmin)
