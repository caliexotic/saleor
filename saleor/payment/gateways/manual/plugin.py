from typing import TYPE_CHECKING

from saleor.payment import TransactionKind
from saleor.payment.interface import GatewayResponse, PaymentData, PaymentMethodInfo
from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField

GATEWAY_NAME = "Manual Payment"

if TYPE_CHECKING:
    from saleor.payment.interface import TokenConfig


class ManualPaymentGatewayPlugin(BasePlugin):
    PLUGIN_ID = "custom.payments.manual"
    PLUGIN_NAME = GATEWAY_NAME
    DEFAULT_ACTIVE = True
    DEFAULT_CONFIGURATION = [
        {"name": "Supported currencies", "value": "USD, EUR, PLN"},
    ]
    CONFIG_STRUCTURE = {
        "Supported currencies": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "Determines currencies supported by the gateway."
            " Please enter currency codes separated by a comma.",
            "label": "Supported currencies",
        },
    }

    def _get_gateway_config(self):
        configuration = {item["name"]: item["value"] for item in self.configuration}
        return {
            "gateway_name": GATEWAY_NAME,
            "supported_currencies": configuration["Supported currencies"],
        }

    def authorize_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        if not self.active:
            return previous_value

        return GatewayResponse(
            is_success=True,
            action_required=False,
            kind=TransactionKind.AUTH,
            amount=payment_information.amount,
            currency=payment_information.currency,
            transaction_id="manual_auth",
            error=None,
            payment_method_info=PaymentMethodInfo(),
        )

    def capture_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        if not self.active:
            return previous_value

        return GatewayResponse(
            is_success=True,
            action_required=False,
            kind=TransactionKind.CAPTURE,
            amount=payment_information.amount,
            currency=payment_information.currency,
            transaction_id="manual_capture",
            error=None,
        )

    def process_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        if not self.active:
            return previous_value

        return self.authorize_payment(payment_information, previous_value)

    def get_supported_currencies(self, previous_value):
        if not self.active:
            return previous_value
        config = self._get_gateway_config()
        return config["supported_currencies"].split(",")

    def get_payment_config(self, previous_value):
        if not self.active:
            return previous_value
        config = self._get_gateway_config()
        return [
            {"field": "supported_currencies", "value": config["supported_currencies"]}
        ]
