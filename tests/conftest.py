import pytest

from src.pay_ccavenue.ccavenue import CCAvenue


@pytest.fixture
def ccavenue_instance():
    return CCAvenue(
        working_key="test_working_key",
        access_code="test_access_code",
        merchant_code="test_merchant_code",
        redirect_url="https://example.com/redirect",
        cancel_url="https://example.com/cancel",
    )
