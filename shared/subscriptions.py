import json
import time
from datetime import UTC, datetime
from typing import Any, Literal, Tuple, TypedDict

import utilities
from appstoreserverlibrary.api_client import AppStoreServerAPIClient
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.HistoryResponse import HistoryResponse
from appstoreserverlibrary.models.TransactionHistoryRequest import (
    Order,
    ProductType,
    TransactionHistoryRequest,
)
from appstoreserverlibrary.receipt_utility import ReceiptUtility
from appstoreserverlibrary.signed_data_verifier import SignedDataVerifier
from attr import asdict
from google.oauth2 import service_account
from googleapiclient.discovery import build

APPLE_PURCHASE_KEY_ID = "5NS8748JDC"
APPLE_ISSUER_ID = "1848d6af-8b85-4906-92ed-2a24766d948e"
APPLE_BUNDLE_ID = "io.vbrato.mobile"
APPLE_APP_ID = 6466803196


ANDROID_PACKAGE_NAME = "io.vbrato.mobile"
ANDROID_SUBSCRIPTION_ID = "vbratotest_2"


def get_apple_server_api_client():
    """
    https://github.com/apple/app-store-server-library-python
    """

    private_key = utilities.get_vbrato_secret("APPLE_INAPP_PURCHASE_KEY", "bytes")

    # TODO: detect environment
    environment = Environment.SANDBOX

    return AppStoreServerAPIClient(
        private_key,
        APPLE_PURCHASE_KEY_ID,
        APPLE_ISSUER_ID,
        APPLE_BUNDLE_ID,
        environment,
    )


def get_apple_jws_data_decoder():
    f1 = utilities.get_vbrato_secret("APPLE_INC_ROOT_CERTIFICATE", "bytes")
    f2 = utilities.get_vbrato_secret("APPLE_COMPUTER_ROOT_CERTIFICATE", "bytes")
    f3 = utilities.get_vbrato_secret("APPLE_ROOT_CA_G2", "bytes")
    f4 = utilities.get_vbrato_secret("APPLE_ROOT_CA_G3", "bytes")

    root_certificates = [f1, f2, f3, f4]

    return SignedDataVerifier(
        root_certificates=root_certificates,
        enable_online_checks=False,
        environment=Environment.SANDBOX,
        bundle_id=APPLE_BUNDLE_ID,
        app_apple_id=APPLE_APP_ID,
    )


def get_google_androidpublisher_service():
    service_account_json = json.loads(
        utilities.get_vbrato_secret("ANDROID_PAYWALL_SERVICE_ACCOUNT")
    )

    credentials = service_account.Credentials.from_service_account_info(
        service_account_json
    )

    return build("androidpublisher", "v3", credentials=credentials)


def get_apple_transactions_from_receipt(receipt: str):
    client = get_apple_server_api_client()
    verifier = get_apple_jws_data_decoder()

    receipt_util = ReceiptUtility()
    app_receipt = receipt

    transactions = []

    try:
        transaction_id = receipt_util.extract_transaction_id_from_app_receipt(
            app_receipt
        )

        if transaction_id is not None:
            response: HistoryResponse | None = None
            request: TransactionHistoryRequest = TransactionHistoryRequest(
                sort=Order.ASCENDING,
                revoked=False,
                productTypes=[ProductType.AUTO_RENEWABLE],
            )
            while response is None or response.hasMore:
                revision = response.revision if response is not None else None
                response = client.get_transaction_history(
                    transaction_id, revision, request
                )
                if response.signedTransactions is None:
                    break
                for signed_transaction in response.signedTransactions:
                    try:
                        transaction_info = (
                            verifier.verify_and_decode_signed_transaction(
                                signed_transaction=signed_transaction
                            )
                        )
                        transactions.append(asdict(transaction_info))
                    except Exception as e:
                        print(e)
                        continue
    except Exception as e:
        print(e)
        return transactions

    return sorted(
        transactions,
        key=lambda transaction: transaction["purchaseDate"],
    )


def is_apple_subscription_active(
    transaction_info: dict,
) -> bool | None:
    """
    transaction_info is a JWSTransactionDecodedPayload with a receipt
    """

    if transaction_info["expiresDate"]:
        current_date = int(time.time() * 1000)
        if current_date > transaction_info["expiresDate"]:
            return False

        return True

    return None


def is_google_subscription_active(subscription_purchase: dict) -> bool | None:
    expiry_datetime = subscription_purchase["lineItems"][0]["expiryTime"]
    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    if expiry_datetime:
        dt_obj = datetime.strptime(expiry_datetime, time_format)
        expiry_time = int(dt_obj.timestamp() * 1000)

        current_date = int(time.time() * 1000)
        if current_date > expiry_time:
            return False

        return True

    return None


def acknowledge_google_subscription(purchase_token: str):
    """
    From https://developer.android.com/google/play/billing/billing_library_overview:
    You must acknowledge all purchases within three days.
    Failure to properly acknowledge purchases results in those purchases being refunded.
    """

    # TODO: use only once instance of the client
    android_publisher = get_google_androidpublisher_service()

    response = (
        android_publisher.purchases()
        .subscriptions()
        .acknowledge(
            packageName=ANDROID_PACKAGE_NAME,
            subscriptionId=ANDROID_SUBSCRIPTION_ID,
            token=purchase_token,
        )
        .execute()
    )
    return response


def get_google_subscription_from_purchase_token(purchase_token: str) -> dict[str, Any]:
    android_publisher = get_google_androidpublisher_service()

    response = (
        android_publisher.purchases()
        .subscriptionsv2()
        .get(
            packageName=ANDROID_PACKAGE_NAME,
            # subscriptionId=ANDROID_SUBSCRIPTION_ID,
            token=purchase_token,
        )
        .execute()
    )
    return response


class ProcessSubscriptionType(TypedDict):
    platform: Literal["ios", "android"]
    user_id: int
    latest_receipt: dict
    product_id: str


def process_subscription(
    session,
    payload: ProcessSubscriptionType,
) -> Tuple[bool, dict]:
    # Apple provides environment, Android doesn't
    environment = ""
    transaction_id = ""
    latest_receipt = payload["latest_receipt"]
    start_date = ""
    end_date = ""
    is_active = ""

    try:
        if payload["platform"] == "ios":
            environment = latest_receipt["environment"]
            transaction_id = latest_receipt["originalTransactionId"]
            latest_receipt = latest_receipt  # ???

            start_date = (
                datetime.fromtimestamp(
                    latest_receipt["originalPurchaseDate"] / 1000, UTC
                ).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                + "Z"
            )

            end_date = (
                datetime.fromtimestamp(
                    latest_receipt["expiresDate"] / 1000, UTC
                ).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                + "Z"
            )

            is_active = is_apple_subscription_active(latest_receipt)

        if payload["platform"] == "android":
            transaction_id = latest_receipt["latestOrderId"]
            latest_receipt = latest_receipt  # ???
            start_date = latest_receipt["startTime"]
            end_date = latest_receipt["lineItems"][0]["expiryTime"]

            is_active = is_google_subscription_active(latest_receipt)

            try:
                acknowledge_response = acknowledge_google_subscription(
                    latest_receipt["purchaseToken"]
                )
                print("Acknoledge response: ", acknowledge_response)
                if acknowledge_response == "":
                    print("Acknowledge is successfull")
            except Exception as e:
                print(e)

        # subscription_exists = (
        #     session.query(Subscription)
        #     .filter(Subscription.originalTransactionId == transaction_id)
        #     .one_or_none()
        # )
        # if not subscription_exists:
        #     subscription = Subscription(
        #         userId=payload["user_id"],
        #         environment=environment,
        #         originalTransactionId=transaction_id,
        #         latestReceipt=latest_receipt,
        #         startDate=utilities.convert_datetime(start_date),
        #         end_date=utilities.convert_datetime(end_date),
        #         platform=payload["platform"],
        #         productId=payload["product_id"],
        #         isActive=is_active,
        #     )
        #     session.add(subscription)
        # else:
        #     subscription = subscription_exists
        #     subscription.isActive = is_active
    except Exception as e:
        print(e)
        return False, {}

    session.commit()

    return True, {
        "userId": payload["user_id"],
        "environment": environment,
        "originalTransactionId": transaction_id,
        "latestReceipt": json.dumps(latest_receipt),
        "startDate": start_date,
        "endDate": end_date,
        "platform": payload["platform"],
        "productId": payload["product_id"],
        "isActive": is_active,
    }
