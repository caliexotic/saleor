import uuid

from ... import ChargeStatus, TransactionKind
from ...interface import GatewayConfig, GatewayResponse, PaymentData, PaymentMethodInfo


def manual_success():
    return True


def get_client_token(**_):
    return str(uuid.uuid4())


def authorize(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    success = manual_success()
    error = None
    if not success:
        error = "Unable to authorize transaction"
    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.AUTH,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id="manual_auth",
        error=error,
        payment_method_info=PaymentMethodInfo(
            last_4=None,
            exp_year=None,
            exp_month=None,
            brand="manual",
            name=payment_information.billing.first_name,
            type="manual",
        ),
    )


def void(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    error = None
    success = manual_success()
    if not success:
        error = "Unable to void the transaction."
    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.VOID,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id="manual_void",
        error=error,
    )


def capture(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform capture transaction."""
    error = None
    success = manual_success()
    if not success:
        error = "Unable to process capture"

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.CAPTURE,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id="manual_capture",
        error=error,
        payment_method_info=PaymentMethodInfo(
            last_4=None,
            exp_year=None,
            exp_month=None,
            brand="manual",
            name=payment_information.billing.first_name,
            type="manual",
        ),
    )


def confirm(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    """Perform confirm transaction."""
    error = None
    success = manual_success()
    if not success:
        error = "Unable to confirm the transaction."

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.CAPTURE,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id="manual_confirm",
        error=error,
    )


def refund(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    error = None
    success = manual_success()
    if not success:
        error = "Unable to process refund"
    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.REFUND,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id="manual_refund",
        error=error,
    )


def process_payment(
    payment_information: PaymentData, config: GatewayConfig
) -> GatewayResponse:
    """Process the payment."""
    authorize_response = authorize(payment_information, config)
    if not config.auto_capture:
        return authorize_response

    capture_response = capture(payment_information, config)
    return capture_response
