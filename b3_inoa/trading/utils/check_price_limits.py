from trading.views import send_price_alert_email


def check_price_limits(asset) -> str:
    last_quotation_price = _get_last_quotation_price(asset)

    if last_quotation_price is None:
        return f"No quotations found for asset {asset.ticker}"

    if _is_below_lower_limit(last_quotation_price, asset.lower_limit):
        _send_buy_alert(asset)
        return f"Buy alert sent for asset {asset.ticker}"

    if _is_above_upper_limit(last_quotation_price, asset.upper_limit):
        _send_sell_alert(asset)
        return f"Sell alert sent for asset {asset.ticker}"

    return "Price is within limits"


def _get_last_quotation_price(asset):
    if last_quotation := asset.quotations.last():
        return last_quotation.price
    return None


def _is_below_lower_limit(price: float, lower_limit: float) -> bool:
    return price <= lower_limit


def _is_above_upper_limit(price: float, upper_limit: float) -> bool:
    return price >= upper_limit


def _send_buy_alert(asset):
    send_price_alert_email(asset, "Buy")


def _send_sell_alert(asset):
    send_price_alert_email(asset, "Sell")
