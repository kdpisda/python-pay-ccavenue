from dataclasses import dataclass
from typing import Optional


@dataclass
class CCavenueWebhookData:
    """
    Represents the data received from a CCAvenue webhook/notification.

    Covers fields for:
    - Order Status (including Reconcilation and Echo)
    - Order Risk Status
    - Payment Type Status
    """

    # Core Fields (Order Status / generic)
    order_id: Optional[str] = None
    tracking_id: Optional[str] = None
    bank_ref_no: Optional[str] = None
    order_status: Optional[str] = None  # Success, Failure, Aborted, Invalid
    failure_message: Optional[str] = None
    payment_mode: Optional[str] = None

    # Card & Bank Details
    card_name: Optional[str] = None
    status_code: Optional[str] = None
    status_message: Optional[str] = None

    # Transaction Details
    currency: Optional[str] = None
    amount: Optional[str] = None

    # Billing Details
    billing_name: Optional[str] = None
    billing_address: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_zip: Optional[str] = None
    billing_country: Optional[str] = None
    billing_tel: Optional[str] = None
    billing_email: Optional[str] = None

    # Delivery Details
    delivery_name: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_city: Optional[str] = None
    delivery_state: Optional[str] = None
    delivery_zip: Optional[str] = None
    delivery_country: Optional[str] = None
    delivery_tel: Optional[str] = None

    # Merchant Custom Fields
    merchant_param1: Optional[str] = None
    merchant_param2: Optional[str] = None
    merchant_param3: Optional[str] = None
    merchant_param4: Optional[str] = None
    merchant_param5: Optional[str] = None

    # Offers & Vault
    vault: Optional[str] = None
    offer_type: Optional[str] = None
    offer_code: Optional[str] = None
    discount_value: Optional[str] = None

    # Risk Status Specific
    risk_status: Optional[str] = None  # High, Low, NR, GA
    risk_reason: Optional[str] = None

    # Payment Type Status Specific
    payment_option: Optional[str] = None
    current_status: Optional[str] = None  # ACTI, FLCT, INAC, DOWN, NEW

    @classmethod
    def from_dict(cls, data: dict) -> "CCavenueWebhookData":
        """
        Create a CCavenueWebhookData instance from a dictionary.
        Keys in the dictionary that don't match fields are ignored.
        """
        # Filter data to only include keys that match field names
        known_fields = set(cls.__annotations__.keys())
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered_data)
