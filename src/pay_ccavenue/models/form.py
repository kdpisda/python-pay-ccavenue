from dataclasses import dataclass


@dataclass
class CCavenueFormData:
    """
    Represents the form data required for CCAvenue payment processing.

    Includes mandatory fields, optional fields, and utility methods for
    data manipulation and validation.
    """

    # Mandatory fields
    merchant_id: str = ""
    order_id: str = ""
    currency: str = "INR"
    amount: str = ""
    redirect_url: str = ""
    cancel_url: str = ""

    # Optional fields
    language: str = "EN"
    billing_name: str = ""
    billing_address: str = ""
    billing_city: str = ""
    billing_state: str = ""
    billing_zip: str = ""
    billing_country: str = ""
    billing_tel: str = ""
    billing_email: str = ""

    shipping_name: str = ""
    shipping_address: str = ""
    shipping_city: str = ""
    shipping_state: str = ""
    shipping_zip: str = ""
    shipping_country: str = ""
    shipping_tel: str = ""

    merchant_param1: str = ""
    merchant_param2: str = ""
    merchant_param3: str = ""
    merchant_param4: str = ""
    merchant_param5: str = ""

    promo_code: str = ""
    customer_identifier: str = ""

    # Additional fields that might be used
    integration_type: str = "iframe_normal"
    mode: str = "LIVE"

    def to_dict(self) -> dict:
        """
        Convert the form data to a dictionary, excluding empty fields.

        Returns:
            dict: A dictionary of non-empty form fields.
        """
        return {k: v for k, v in self.__dict__.items() if v}

    def validate(self) -> None:
        """
        Validate the mandatory fields of the form data.

        Raises:
            ValueError: If any mandatory field is empty.
        """
        mandatory_fields = [
            "merchant_id",
            "order_id",
            "currency",
            "amount",
            "redirect_url",
            "cancel_url",
        ]
        for field in mandatory_fields:
            if not getattr(self, field):
                raise ValueError(f"{field} is mandatory and cannot be empty")

    @classmethod
    def from_dict(cls, data: dict) -> "CCavenueFormData":
        """
        Create a CCavenueFormData instance from a dictionary.

        Args:
            data (dict): A dictionary containing form data.

        Returns:
            CCavenueFormData: An instance of CCavenueFormData.
        """
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
