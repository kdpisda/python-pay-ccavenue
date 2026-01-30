from pay_ccavenue.models.webhook import CCavenueWebhookData


def test_webhook_data_from_dict():
    """Test that CCavenueWebhookData correctly parses a dictionary."""
    data = {
        "order_id": "123",
        "order_status": "Success",
        "amount": "100.00",
        "unknown_field": "should_be_ignored",
        "merchant_param1": "custom_data",
    }

    webhook_data = CCavenueWebhookData.from_dict(data)

    assert webhook_data.order_id == "123"
    assert webhook_data.order_status == "Success"
    assert webhook_data.amount == "100.00"
    assert webhook_data.merchant_param1 == "custom_data"

    # Check that unknown fields are ignored (not present as attributes)
    # Dataclasses only have defined fields
    assert not hasattr(webhook_data, "unknown_field")


def test_process_webhook(ccavenue_instance, monkeypatch):
    """Test the process_webhook method of CCAvenue class."""

    # Mock decrypt to return a specific dictionary
    expected_dict = {
        "order_id": "ORDER123",
        "tracking_id": "TRACK123",
        "order_status": "Success",
        "amount": "500.50",
        "currency": "INR",
        "payment_mode": "Net Banking",
        "card_name": "HDFC",
    }

    def mock_decrypt(data):
        return expected_dict

    monkeypatch.setattr(ccavenue_instance, "decrypt", mock_decrypt)

    # The input to process_webhook is a dict with 'encResp'
    # Since we mocked decrypt, the content doesn't matter much, but structure does
    dummy_input = {"encResp": "dummy_encrypted_string"}

    result = ccavenue_instance.process_webhook(dummy_input)

    assert isinstance(result, CCavenueWebhookData)
    assert result.order_id == "ORDER123"
    assert result.tracking_id == "TRACK123"
    assert result.order_status == "Success"
    assert result.amount == "500.50"
    assert result.currency == "INR"
    assert result.payment_mode == "Net Banking"
    assert result.card_name == "HDFC"
    # Ensure optional fields are None
    assert result.failure_message is None
