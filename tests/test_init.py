import os

import pytest


def test_init(ccavenue_instance):
    assert ccavenue_instance._CCAvenue__WORKING_KEY == "test_working_key"
    assert ccavenue_instance._CCAvenue__ACCESS_CODE == "test_access_code"
    assert ccavenue_instance._CCAvenue__MERCHANT_CODE == "test_merchant_code"
    assert ccavenue_instance._CCAvenue__REDIRECT_URL == "https://example.com/redirect"
    assert ccavenue_instance._CCAvenue__CANCEL_URL == "https://example.com/cancel"


def test_load_working_key(ccavenue_instance):
    ccavenue_instance.load_working_key("new_working_key")
    assert ccavenue_instance._CCAvenue__WORKING_KEY == "new_working_key"

    os.environ["CCAVENUE_WORKING_KEY"] = "env_working_key"
    ccavenue_instance.load_working_key()
    assert ccavenue_instance._CCAvenue__WORKING_KEY == "env_working_key"

    with pytest.raises(ValueError):
        ccavenue_instance.load_working_key(None)
        os.environ.pop("CCAVENUE_WORKING_KEY")
        ccavenue_instance.load_working_key()


def test_load_access_code(ccavenue_instance):
    ccavenue_instance.load_access_code("new_access_code")
    assert ccavenue_instance._CCAvenue__ACCESS_CODE == "new_access_code"

    os.environ["CCAVENUE_ACCESS_CODE"] = "env_access_code"
    ccavenue_instance.load_access_code()
    assert ccavenue_instance._CCAvenue__ACCESS_CODE == "env_access_code"

    with pytest.raises(ValueError):
        ccavenue_instance.load_access_code(None)
        os.environ.pop("CCAVENUE_ACCESS_CODE")
        ccavenue_instance.load_access_code()


def test_load_merchant_code(ccavenue_instance):
    ccavenue_instance.load_merchant_code("new_merchant_code")
    assert ccavenue_instance._CCAvenue__MERCHANT_CODE == "new_merchant_code"

    os.environ["CCAVENUE_MERCHANT_CODE"] = "env_merchant_code"
    ccavenue_instance.load_merchant_code()
    assert ccavenue_instance._CCAvenue__MERCHANT_CODE == "env_merchant_code"

    with pytest.raises(ValueError):
        ccavenue_instance.load_merchant_code(None)
        os.environ.pop("CCAVENUE_MERCHANT_CODE")
        ccavenue_instance.load_merchant_code()


def test_load_redirect_url(ccavenue_instance):
    ccavenue_instance.load_redirect_url("https://new.example.com/redirect")
    assert (
        ccavenue_instance._CCAvenue__REDIRECT_URL == "https://new.example.com/redirect"
    )
    assert (
        ccavenue_instance._CCAvenue__form_data["redirect_url"]
        == "https://new.example.com/redirect"
    )

    os.environ["CCAVENUE_REDIRECT_URL"] = "https://env.example.com/redirect"
    ccavenue_instance.load_redirect_url(None)
    assert (
        ccavenue_instance._CCAvenue__REDIRECT_URL == "https://env.example.com/redirect"
    )
    assert (
        ccavenue_instance._CCAvenue__form_data["redirect_url"]
        == "https://env.example.com/redirect"
    )

    with pytest.raises(ValueError):
        ccavenue_instance.load_redirect_url(None)
        os.environ.pop("CCAVENUE_REDIRECT_URL")
        ccavenue_instance.load_redirect_url(None)


def test_load_cancel_url(ccavenue_instance):
    ccavenue_instance.load_cancel_url("https://new.example.com/cancel")
    assert ccavenue_instance._CCAvenue__CANCEL_URL == "https://new.example.com/cancel"
    assert (
        ccavenue_instance._CCAvenue__form_data["cancel_url"]
        == "https://new.example.com/cancel"
    )

    os.environ["CCAVENUE_CANCEL_URL"] = "https://env.example.com/cancel"
    ccavenue_instance.load_cancel_url(None)
    assert ccavenue_instance._CCAvenue__CANCEL_URL == "https://env.example.com/cancel"
    assert (
        ccavenue_instance._CCAvenue__form_data["cancel_url"]
        == "https://env.example.com/cancel"
    )

    with pytest.raises(ValueError):
        ccavenue_instance.load_cancel_url(None)
        os.environ.pop("CCAVENUE_CANCEL_URL")
        ccavenue_instance.load_cancel_url(None)
