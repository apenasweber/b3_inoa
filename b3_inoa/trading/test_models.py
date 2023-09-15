import pytest

from .models import Asset, Quotation
from .views import send_email_alert


@pytest.mark.django_db
def test_send_email_alert(mocker):
    mocker.patch("trading.views.send_mail")
    asset = Asset.objects.create(
        ticker="ABC1",
        lower_limit=10.0,
        upper_limit=20.0,
        check_interval=30,
        email="test@example.com",
    )
    send_email_alert(asset, "Buy")


@pytest.mark.django_db
def test_asset_creation():
    asset = Asset.objects.create(
        ticker="ABC2",
        lower_limit=10.0,
        upper_limit=20.0,
        check_interval=30,
        email="test@example.com",
    )
    assert asset.ticker == "ABC2"
    assert asset.lower_limit == 10.0
    assert asset.upper_limit == 20.0


@pytest.mark.django_db
def test_quotation_creation():
    asset = Asset.objects.create(
        ticker="ABC3",
        lower_limit=10.0,
        upper_limit=20.0,
        check_interval=30,
        email="test@example.com",
    )
    quotation = Quotation.objects.create(asset=asset, price=15.0)
    assert quotation.asset == asset
    assert quotation.price == 15.0
