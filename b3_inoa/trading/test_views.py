import pytest

from .models import Asset
from .views import send_email_alert


@pytest.mark.django_db
def test_send_email_alert(mocker):
    mocker.patch("trading.views.send_mail")
    asset = Asset.objects.create(
        ticker="ABC",
        lower_limit=10.0,
        upper_limit=20.0,
        check_interval=30,
        email="test@example.com",
    )
    send_email_alert(asset, "Buy")
