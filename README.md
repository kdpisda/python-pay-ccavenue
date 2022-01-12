# pay_ccavenue

A simple package to integrate CCAvenue.

## How to install

```bash
pip install pay_ccavenue
```

## Import

```python
from pay_ccavenue import CCAvenue
```

## Initialize the Package

We can either setup via the environment or by passing the credentials directly to the plugin.

### Via the environment variables

Set the credentials in the environment variables

- Set `CCAVENUE_WORKING_KEY` for the `WORKING_KEY`
- Set `CCAVENUE_ACCESS_CODE` for the `ACCESS_CODE`
- Set `CCAVENUE_MERCHANT_CODE` for the `MERCHANT_CODE`

And then instantiate the `CCAvenue` object as shown below

```python
ccavenue = CCAvenue()
```

### Pasing the credentials directly

```python
ccavenue = CCAvenue(WORKING_KEY, ACCESS_CODE, MERCHANT_CODE)
```

## To encrypt the data

`form_data` is the post request body which is a dictionary of the related data for the payment. You don't need to pass the Merchant ID though. Since we have already intiated the package with the correct `MERCHANT_CODE`. `encrypt()` method return the encrypted string that can be ussed directly in the Iframe rendering.

```python
encrypt_data = ccavenue.encrypt(form_data)
```

Pass the `encrypt_data` from the above to the view to render the IFrame.

## Decrypt the data received from the CCAvenue

`form_data` is the post request body which is a dictionary of the related data received from the CCAvenue. The `decrypt()` method returns the dictionary of the data received from the CCAvenue.

```python
decrypted_data = ccavenue.decrypt(form_data)
```

# Limitations

1. I have not added any tests as of now in the package, but I have tested this out for my project after debugging their given examples and Stackoverflow to simplify it.
2. More detailed documentation.
3. Currently supports only Iframe method.
