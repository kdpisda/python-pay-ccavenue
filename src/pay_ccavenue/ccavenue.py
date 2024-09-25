import hashlib
import os
from binascii import hexlify
from binascii import unhexlify
from typing import Any
from typing import Dict

from Crypto.Cipher import AES
from pay_ccavenue.models.config import CCavenueConfig
from pay_ccavenue.models.form import CCavenueFormData


class CCAvenue:
    """Handles CCAvenue payment gateway operations."""

    _IV = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"

    def __init__(
        self,
        working_key=None,
        access_code=None,
        merchant_code=None,
        redirect_url=None,
        cancel_url=None,
    ):
        """
        Initialize CCAvenue with credentials.

        Uses provided parameters or falls back to environment variables:
        - CCAVENUE_WORKING_KEY
        - CCAVENUE_ACCESS_CODE
        - CCAVENUE_MERCHANT_CODE
        - CCAVENUE_REDIRECT_URL
        - CCAVENUE_CANCEL_URL
        """
        self.config = CCavenueConfig(
            working_key=working_key or os.environ.get("CCAVENUE_WORKING_KEY"),
            access_code=access_code or os.environ.get("CCAVENUE_ACCESS_CODE"),
            merchant_code=merchant_code or os.environ.get("CCAVENUE_MERCHANT_CODE"),
            redirect_url=redirect_url or os.environ.get("CCAVENUE_REDIRECT_URL"),
            cancel_url=cancel_url or os.environ.get("CCAVENUE_CANCEL_URL"),
        )
        self.config.validate()
        self.form_data = CCavenueFormData()
        self.response_body = {"encResp": ""}
        self.decrypted_data = {}

    def _get_cipher(self) -> AES:
        """
        Create and return an AES cipher object.

        Returns:
            AES: An AES cipher object initialized with the working key and IV.

        Note:
            This method uses MD5 to hash the working key. While MD5 is not
            cryptographically secure, it's used here to maintain compatibility
            with CCAvenue's implementation.
        """
        key = hashlib.md5(self.config.working_key.encode()).digest()
        return AES.new(key, AES.MODE_CBC, self._IV)

    def _pad(self, data: str) -> str:
        """
        Pad the input data to be a multiple of 16 bytes.

        Args:
            data (str): The data to be padded.

        Returns:
            str: The padded data.

        Note:
            This method uses PKCS7 padding.
        """
        length = 16 - (len(data) % 16)
        return data + (chr(length) * length)

    def _parse_request_body(self, request_body: Dict[str, Any]) -> str:
        """
        Parse the request body and prepare it for encryption.

        Args:
            request_body (Dict[str, Any]): The request body to be parsed.

        Returns:
            str: A string representation of the parsed request body.

        Note:
            This method also sets some default values from the config.
        """
        self.form_data = CCavenueFormData.from_dict(request_body)
        self.form_data.merchant_id = self.config.merchant_code
        self.form_data.redirect_url = self.config.redirect_url
        self.form_data.cancel_url = self.config.cancel_url
        return "&".join(
            f"{key}={value}" for key, value in self.form_data.to_dict().items()
        )

    def _validate_request_body(self) -> None:
        """
        Validate the request body.

        Raises:
            ValueError: If the amount is not a valid float.

        Note:
            This method calls the form_data's validate method and additionally
            checks if the amount is a valid float.
        """
        self.form_data.validate()
        try:
            float(self.form_data.amount)
        except ValueError:
            raise ValueError("You must provide a valid amount for CCAvenue.")

    def encrypt(self, data: Dict[str, Any]) -> str:
        """
        Encrypt the request data for CCAvenue.

        Args:
            data (Dict[str, Any]): The data to be encrypted.

        Returns:
            str: The encrypted data as a hexadecimal string.

        Note:
            This method handles the entire encryption process including
            parsing, validation, padding, and encryption.
        """
        parsed_data = self._parse_request_body(data)
        self._validate_request_body()
        padded_data = self._pad(parsed_data)
        cipher = self._get_cipher()
        encrypted = cipher.encrypt(padded_data.encode("utf-8"))
        return hexlify(encrypted).decode("utf-8")

    def _parse_response_body(self, response_body: Dict[str, str]) -> bytes:
        """
        Parse and validate the response body from CCAvenue.

        Args:
            response_body (Dict[str, str]): The response body from CCAvenue.

        Returns:
            bytes: The encrypted response as bytes.

        Raises:
            ValueError: If the response body is invalid.

        Note:
            This method expects the response body to contain an 'encResp' key
            with a string value.
        """
        if not isinstance(response_body.get("encResp"), str):
            raise ValueError("You must provide a valid response body for CCAvenue.")
        self.response_body = response_body
        return unhexlify(response_body["encResp"])

    def _unflatten_decrypted_data(self, data: bytes) -> None:
        """
        Convert the decrypted data from a flat string to a dictionary.

        Args:
            data (bytes): The decrypted data as bytes.

        Note:
            This method splits the decrypted data on '&' and '=' characters
            to create key-value pairs.
        """
        self.decrypted_data = dict(
            item.split("=") for item in data.decode("utf-8").split("&") if item
        )

    def decrypt(self, data: Dict[str, str]) -> Dict[str, str]:
        """
        Decrypt the response data from CCAvenue.

        Args:
            data (Dict[str, str]): The encrypted response data.

        Returns:
            Dict[str, str]: The decrypted data as a dictionary.

        Note:
            This method handles the entire decryption process including
            parsing the response body, decryption, and unflattening the data.
        """
        encrypted_text = self._parse_response_body(data)
        cipher = self._get_cipher()
        decrypted = cipher.decrypt(encrypted_text)
        self._unflatten_decrypted_data(decrypted)
        return self.decrypted_data
