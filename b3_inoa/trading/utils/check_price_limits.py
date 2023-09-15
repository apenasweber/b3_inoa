def check_price_limits(asset) -> str:
    from trading.views import send_email_alert

    last_quotation = asset.quotations.last()
    if last_quotation is None:
        return f"No quotations found for asset {asset.ticker}"

    current_price = last_quotation.price

    if current_price <= asset.lower_limit:
        send_email_alert(asset, "Buy")
        return f"Buy alert sent for asset {asset.ticker}"

    elif current_price >= asset.upper_limit:
        send_email_alert(asset, "Sell")
        return f"Sell alert sent for asset {asset.ticker}"

    return "Price is within limits"
