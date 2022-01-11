import hashlib
import os
from binascii import hexlify
from binascii import unhexlify

from Crypto.Cipher import AES


class CCAvenue:
    __WORKING_KEY: str = None
    __ACCESS_CODE: str = None
    __MERCHANT_CODE: str = None
    __iv = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
    __form_data = {
        "order_id": "",
        "currency": "",
        "amount": "",
        "redirect_url": "",
        "cancel_url": "",
        "language": "",
        "billing_name": "",
        "billing_address": "",
        "billing_city": "",
        "billing_state": "",
        "billing_zip": "",
        "billing_country": "",
        "billing_tel": "",
        "billing_email": "",
        "delivery_name": "",
        "delivery_address": "",
        "delivery_city": "",
        "delivery_state": "",
        "delivery_zip": "",
        "delivery_country": "",
        "delivery_tel": "",
        "merchant_param1": "",
        "merchant_param2": "",
        "merchant_param3": "",
        "merchant_param4": "",
        "merchant_param5": "",
        "integration_type": "",
        "promo_code": "",
        "customer_identifier": "",
    }

    __response_body = {"encResp": ""}
    __descrypted_data = {}

    def __init__(
        self,
        working_key: str = None,
        access_code: str = None,
        merchant_code: str = None,
    ) -> None:
        """
        Initialize the CCAvenue class.

        :param working_key: The working key for the CCAvenue gateway.
        :param access_code: The access code for the CCAvenue gateway.
        :param merchant_code: The merchant code for the CCAvenue gateway.
        """
        self.load_working_key(working_key)
        self.load_access_code(access_code)
        self.load_merchant_code(merchant_code)

    def load_working_key(self, working_key: str = None) -> None:
        """
        Load a working key into the CCAvenue class.

        :param working_key: The working key for the CCAvenue gateway.
        """
        if working_key:
            self.__WORKING_KEY = working_key
        else:
            self.__WORKING_KEY = os.environ.get("CCAVENUE_WORKING_KEY")

        if self.__WORKING_KEY is None or isinstance(self.__WORKING_KEY, str) is False:
            raise ValueError(
                "You must provide a working key for CCAvenue or set working key as "
                "an environment variable by setting it as CCAVENUE_WORKING_KEY."
            )

    def load_access_code(self, access_code: str = None) -> None:
        """
        Load an access code into the CCAvenue class.

        :param access_code: The access code for the CCAvenue gateway.
        """
        if access_code:
            self.__ACCESS_CODE = access_code
        else:
            self.__ACCESS_CODE = os.environ.get("CCAVENUE_ACCESS_CODE")

        if self.__ACCESS_CODE is None or isinstance(self.__ACCESS_CODE, str) is False:
            raise ValueError(
                "You must provide an access code for CCAvenue or set access code "
                "as an environment variable by setting it as CCAVENUE_ACCESS_CODE."
            )

    def load_merchant_code(self, merchant_code: str = None) -> None:
        """
        Load a merchant code into the CCAvenue class.

        :param merchant_code: The merchant code for the CCAvenue gateway.
        """
        if merchant_code:
            self.__MERCHANT_CODE = merchant_code
        else:
            self.__MERCHANT_CODE = os.environ.get("CCAVENUE_MERCHANT_CODE")

        if (
            self.__MERCHANT_CODE is None
            or isinstance(self.__MERCHANT_CODE, str) is False
        ):
            raise ValueError(
                "You must provide a merchant code for CCAvenue or set merchant "
                "code as an environment variable by setting it as CCAVENUE_MERCHANT_CODE."
            )

    def pad(self, data: str):
        """
        Pad the data to be encrypted.

        :param data: The str data to be encrypted.
        """
        length = 16 - (len(data) % 16)
        data += chr(length) * length
        return data

    def validate_request_body(self) -> None:
        """
        Validate the request body.

        :param data: The request body to be validated.
        """
        if (
            self.__form_data["order_id"] is None
            or isinstance(self.__form_data["order_id"], str) is False
        ):
            raise ValueError("You must provide an order id for CCAvenue.")

        if (
            self.__form_data["currency"] is None
            or isinstance(self.__form_data["currency"], str) is False
        ):
            raise ValueError("You must provide a currency for CCAvenue.")

        if self.__form_data["amount"] is None:
            raise ValueError("You must provide an amount for CCAvenue.")
        else:
            try:
                float(self.__form_data["amount"])
            except ValueError:
                raise ValueError("You must provide a valid amount for CCAvenue.")

        if (
            self.__form_data["redirect_url"] is None
            or isinstance(self.__form_data["redirect_url"], str) is False
        ):
            raise ValueError("You must provide a valid redirect url for CCAvenue.")

        if (
            self.__form_data["cancel_url"] is None
            or isinstance(self.__form_data["cancel_url"], str) is False
        ):
            raise ValueError("You must provide a valid cancel url for CCAvenue.")

        if (
            self.__form_data["billing_name"] is None
            or isinstance(self.__form_data["billing_name"], str) is False
        ):
            raise ValueError("You must provide a billing name for CCAvenue.")

        if (
            self.__form_data["billing_tel"] is None
            or isinstance(self.__form_data["billing_tel"], str) is False
        ):
            raise ValueError("You must provide a billing tel for CCAvenue.")

        if (
            self.__form_data["billing_email"] is None
            or isinstance(self.__form_data["billing_email"], str) is False
        ):
            raise ValueError("You must provide a billing tel for CCAvenue.")

    def parse_request_body(self, request_body: dict) -> str:
        """
        Parse the request body to be encrypted.

        :param request_body: The request body to be encrypted.

        :return: The request body in str to be encrypted.
        """
        self.__form_data = {**self.__form_data, **request_body}
        form_str = f"merchant_id={self.__MERCHANT_CODE}"
        for key, value in self.__form_data.items():
            form_str += "&" + key + "=" + value
        return form_str

    def __get_cipher(self) -> AES:
        """
        Get the cipher object.

        :param key: The key to be used for encryption.
        """
        bytearrayWorkingKey = bytearray()
        bytearrayWorkingKey.extend(map(ord, self.__WORKING_KEY))
        return AES.new(
            hashlib.md5(bytearrayWorkingKey).digest(),
            AES.MODE_CBC,
            self.__iv.encode("utf-8"),
        )

    def encrypt(self, data: dict) -> bytearray:
        """
        Encrypt the data to be sent to CCAvenue.

        :param data: The data to be encrypted.

        :return: The encrypted data.
        """
        data = self.parse_request_body(data)
        self.validate_request_body()
        data = self.pad(data)
        enc_cipher = self.__get_cipher()
        return hexlify(enc_cipher.encrypt(data.encode("utf-8"))).decode("utf-8")

    def parse_response_body(self, response_body: str) -> str:
        """
        Parse the response body to be decrypted.

        :param response_body: The response body to be decrypted.

        :return: The decrypted response body.
        """
        if (
            response_body.get("encResp") is None
            or isinstance(response_body.get("encResp"), str) is False
        ):
            raise ValueError("You must provide a valid response body for CCAvenue.")
        else:
            self.__response_body = response_body
        return unhexlify(response_body.get("encResp"))

    def unflatten_descrypted_data(self, data: bytearray) -> None:
        """
        Unflatten the decrypted data.

        :param data: The decrypted data.

        :return: The unflattened data.
        """
        self.__descrypted_data = dict(
            item.split("=") for item in data.decode("utf-8").split("&") if item
        )

    def decrypt(self, data: dict) -> str:
        """
        Decrypt the data received from CCAvenue.

        :param data: The data to be decrypted.

        :return: The decrypted data.
        """
        encryptedText = self.parse_response_body(data)
        dec_cipher = self.__get_cipher()
        self.unflatten_descrypted_data(dec_cipher.decrypt(encryptedText))
        return self.__descrypted_data
