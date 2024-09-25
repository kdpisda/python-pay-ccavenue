from dataclasses import dataclass


@dataclass
class CCavenueConfig:
    """
    A class to store and validate CCAvenue configuration.

    This class holds the necessary configuration parameters for CCAvenue integration
    and provides a method to validate that all required fields are present.

    Attributes:
        working_key (str): CCAvenue working key.
        access_code (str): CCAvenue access code.
        merchant_code (str): CCAvenue merchant code.
        redirect_url (str): URL to redirect after successful payment.
        cancel_url (str): URL to redirect after cancelled payment.
    """

    def __init__(
        self, working_key, access_code, merchant_code, redirect_url, cancel_url
    ):
        """
        Initialize the CCavenueConfig instance.

        Args:
            working_key (str): CCAvenue working key.
            access_code (str): CCAvenue access code.
            merchant_code (str): CCAvenue merchant code.
            redirect_url (str): URL to redirect after successful payment.
            cancel_url (str): URL to redirect after cancelled payment.
        """
        self.working_key = working_key
        self.access_code = access_code
        self.merchant_code = merchant_code
        self.redirect_url = redirect_url
        self.cancel_url = cancel_url

    def validate(self):
        """
        Validate that all required fields are present.

        Raises:
            ValueError: If any required field is missing.
        """
        required_fields = [
            "working_key",
            "access_code",
            "merchant_code",
            "redirect_url",
            "cancel_url",
        ]
        missing_fields = [
            field for field in required_fields if not getattr(self, field)
        ]
        if missing_fields:
            raise ValueError(
                "The following fields must be provided or set as environment "
                f"variables: {', '.join(missing_fields)}"
            )
