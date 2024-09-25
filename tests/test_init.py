import pytest

from src.pay_ccavenue.ccavenue import CCAvenue


def test_init(ccavenue_instance):
    assert ccavenue_instance.config.working_key == "test_working_key"
    assert ccavenue_instance.config.access_code == "test_access_code"
    assert ccavenue_instance.config.merchant_code == "test_merchant_code"
    assert ccavenue_instance.config.redirect_url == "https://example.com/redirect"
    assert ccavenue_instance.config.cancel_url == "https://example.com/cancel"


def test_init_with_env_variables(monkeypatch):
    # Set environment variables
    monkeypatch.setenv("CCAVENUE_WORKING_KEY", "env_working_key")
    monkeypatch.setenv("CCAVENUE_ACCESS_CODE", "env_access_code")
    monkeypatch.setenv("CCAVENUE_MERCHANT_CODE", "env_merchant_code")
    monkeypatch.setenv("CCAVENUE_REDIRECT_URL", "https://env.example.com/redirect")
    monkeypatch.setenv("CCAVENUE_CANCEL_URL", "https://env.example.com/cancel")

    # Initialize CCAvenue without passing any parameters
    ccavenue = CCAvenue()

    # Assert that the values are loaded from environment variables
    assert ccavenue.config.working_key == "env_working_key"
    assert ccavenue.config.access_code == "env_access_code"
    assert ccavenue.config.merchant_code == "env_merchant_code"
    assert ccavenue.config.redirect_url == "https://env.example.com/redirect"
    assert ccavenue.config.cancel_url == "https://env.example.com/cancel"


def test_init_missing_values():
    with pytest.raises(ValueError):
        CCAvenue()


def test_init_partial_values():
    with pytest.raises(ValueError):
        CCAvenue(working_key="test_working_key")


def test_init_priority(monkeypatch):
    # Set environment variables
    monkeypatch.setenv("CCAVENUE_WORKING_KEY", "env_working_key")
    monkeypatch.setenv("CCAVENUE_ACCESS_CODE", "env_access_code")
    monkeypatch.setenv("CCAVENUE_MERCHANT_CODE", "env_merchant_code")
    monkeypatch.setenv("CCAVENUE_REDIRECT_URL", "https://env.example.com/redirect")
    monkeypatch.setenv("CCAVENUE_CANCEL_URL", "https://env.example.com/cancel")

    # Initialize CCAvenue with some parameters
    ccavenue = CCAvenue(
        working_key="param_working_key", access_code="param_access_code"
    )

    # Assert that passed parameters take priority over environment variables
    assert ccavenue.config.working_key == "param_working_key"
    assert ccavenue.config.access_code == "param_access_code"
    # These should still be from environment variables
    assert ccavenue.config.merchant_code == "env_merchant_code"
    assert ccavenue.config.redirect_url == "https://env.example.com/redirect"
    assert ccavenue.config.cancel_url == "https://env.example.com/cancel"
