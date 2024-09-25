import pytest
from Crypto.Cipher import AES


def test_pad(ccavenue_instance):
    assert ccavenue_instance._pad("1234567890123") == "1234567890123\x03\x03\x03"
    assert (
        ccavenue_instance._pad("1234567890123456")
        == "1234567890123456\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"  # noqa
    )


def test_validate_request_body(ccavenue_instance):
    valid_data = {
        "order_id": "123",
        "currency": "INR",
        "amount": "100.00",
        "billing_name": "John Doe",
        "billing_tel": "1234567890",
        "billing_email": "john@example.com",
    }
    ccavenue_instance._parse_request_body(valid_data)
    ccavenue_instance._validate_request_body()  # Should not raise any exception

    invalid_cases = [
        {"order_id": None},
        {"currency": None},
        {"amount": None},
        {"amount": "invalid"},
    ]

    for invalid_data in invalid_cases:
        invalid_request = valid_data.copy()
        invalid_request.update(invalid_data)
        ccavenue_instance._parse_request_body(invalid_request)
        with pytest.raises(ValueError):
            ccavenue_instance._validate_request_body()


def test_parse_request_body(ccavenue_instance):
    request_body = {
        "order_id": "123",
        "currency": "INR",
        "amount": "100.00",
    }
    result = ccavenue_instance._parse_request_body(request_body)
    assert "merchant_id=test_merchant_code" in result
    assert "order_id=123" in result
    assert "currency=INR" in result
    assert "amount=100.00" in result


def test_encrypt(ccavenue_instance, monkeypatch):
    def mock_get_cipher():
        return AES.new(b"1234567890123456", AES.MODE_CBC, b"1234567890123456")

    monkeypatch.setattr(ccavenue_instance, "_get_cipher", mock_get_cipher)

    request_data = {
        "order_id": "123",
        "currency": "INR",
        "amount": "100.00",
        "billing_name": "John Doe",
        "billing_tel": "1234567890",
        "billing_email": "john@example.com",
    }

    encrypted_data = ccavenue_instance.encrypt(request_data)
    assert isinstance(encrypted_data, str)
    assert len(encrypted_data) > 0


def test_parse_response_body(ccavenue_instance):
    valid_response = {"encResp": "48656c6c6f20576f726c64"}  # "Hello World" in hex
    result = ccavenue_instance._parse_response_body(valid_response)
    assert result == b"Hello World"

    with pytest.raises(ValueError):
        ccavenue_instance._parse_response_body({"invalid_key": "value"})


def test_unflatten_decrypted_data(ccavenue_instance):
    decrypted_data = b"key1=value1&key2=value2&key3=value3"
    ccavenue_instance._unflatten_decrypted_data(decrypted_data)
    assert ccavenue_instance.decrypted_data == {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }


def test_decrypt(ccavenue_instance, monkeypatch):
    def mock_get_cipher():
        return AES.new(b"1234567890123456", AES.MODE_CBC, b"1234567890123456")

    monkeypatch.setattr(ccavenue_instance, "_get_cipher", mock_get_cipher)

    # Encrypt a sample string
    sample_data = "key1=value1&key2=value2&key3=value3"
    encrypted_data = AES.new(
        b"1234567890123456", AES.MODE_CBC, b"1234567890123456"
    ).encrypt(ccavenue_instance._pad(sample_data).encode("utf-8"))

    response_data = {"encResp": encrypted_data.hex()}
    decrypted_data = ccavenue_instance.decrypt(response_data)

    # Remove padding from the decrypted values
    decrypted_data = {k: v.rstrip("\r") for k, v in decrypted_data.items()}

    assert decrypted_data == {"key1": "value1", "key2": "value2", "key3": "value3"}
