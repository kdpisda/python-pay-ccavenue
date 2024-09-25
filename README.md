# pay_ccavenue

A Python package for seamless integration with CCAvenue payment gateway.

## Features

- Easy-to-use API for CCAvenue integration
- Secure encryption and decryption of payment data
- Flexible configuration via environment variables or direct instantiation
- Type hints for better code reliability

## Current Limitations

- This package does not yet support iframe integration with CCAvenue. It currently provides basic encryption and decryption functionality for standard integration.

## Installation

Install the package using pip:

```bash
pip install pay_ccavenue
```

## Quick Start

1. Import the CCAvenue class:

```python
from pay_ccavenue import CCAvenue
```

2. Initialize the CCAvenue object:

```python
# Using environment variables
ccavenue = CCAvenue()

# Or, passing credentials directly
ccavenue = CCAvenue(
    working_key="YOUR_WORKING_KEY",
    access_code="YOUR_ACCESS_CODE",
    merchant_code="YOUR_MERCHANT_CODE",
    redirect_url="YOUR_REDIRECT_URL",
    cancel_url="YOUR_CANCEL_URL"
)
```

3. Encrypt payment data:

```python
form_data = {
    "order_id": "123456",
    "amount": "1000.00",
    "currency": "INR",
    # Add other required fields
}

encrypted_data = ccavenue.encrypt(form_data)
```

4. Decrypt response data:

```python
response_data = {
    "encResp": "ENCRYPTED_RESPONSE_FROM_CCAVENUE"
}

decrypted_data = ccavenue.decrypt(response_data)
```

## Configuration

### Environment Variables

Set the following environment variables to configure the package:

- `CCAVENUE_WORKING_KEY`: Your CCAvenue working key
- `CCAVENUE_ACCESS_CODE`: Your CCAvenue access code
- `CCAVENUE_MERCHANT_CODE`: Your CCAvenue merchant code
- `CCAVENUE_REDIRECT_URL`: URL to redirect after successful payment
- `CCAVENUE_CANCEL_URL`: URL to redirect after cancelled payment

### Direct Instantiation

Pass the configuration parameters directly when creating the CCAvenue object:

```python
ccavenue = CCAvenue(
    working_key="YOUR_WORKING_KEY",
    access_code="YOUR_ACCESS_CODE",
    merchant_code="YOUR_MERCHANT_CODE",
    redirect_url="YOUR_REDIRECT_URL",
    cancel_url="YOUR_CANCEL_URL"
)
```

## API Reference

### `CCAvenue` Class

#### Methods

- `encrypt(data: Dict[str, Any]) -> str`: Encrypts the payment data
- `decrypt(data: Dict[str, str]) -> Dict[str, str]`: Decrypts the response data

### `CCavenueFormData` Class

Represents the form data required for CCAvenue payment processing. It includes mandatory and optional fields, and provides methods for data manipulation and validation.

#### Important Fields

- `merchant_id`: CCAvenue merchant ID
- `order_id`: Unique order identifier
- `currency`: Payment currency (default: "INR")
- `amount`: Payment amount
- `redirect_url`: URL for successful payment redirection
- `cancel_url`: URL for cancelled payment redirection

For a complete list of fields, refer to the `CCavenueFormData` class documentation.

## Security Considerations

- The package uses AES encryption with CBC mode for secure communication with CCAvenue.
- Ensure that your working key and other sensitive information are kept secure and not exposed in your codebase.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This package is not officially associated with CCAvenue. Use it at your own risk and ensure compliance with CCAvenue's terms of service.
