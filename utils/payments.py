from typing import Dict, Optional
from datetime import datetime, timedelta
import requests
import logging
from auth.usps_oauth import USPSOAuth2

# Configure logging for the payments module
logger = logging.getLogger(__name__)


class USPSPayments:
    """Handles USPS payment operations including authorization and token management"""

    PAYMENT_AUTH_ENDPOINT = "https://apis-tem.usps.com/payments/v3/payment-authorization"
    OAUTH_TOKEN_URL = "https://apis.usps.com/oauth2/v3/token"

    def __init__(self):
        """Initialize the payments client with its own OAuth manager"""
        logger.info("Initializing USPS Payments client")
        self.oauth_client = USPSOAuth2(self.OAUTH_TOKEN_URL)
        # Clear any existing tokens on initialization
        self.oauth_client.clear_token()

    def get_payment_authorization(self) -> Dict:
        """
        Obtain a payment authorization token from USPS

        Returns:
            Dict: Payment authorization response containing the token and other details

        Raises:
            ValueError: If the request fails or returns an error
        """
        logger.info("Requesting payment authorization token")

        # Get a valid OAuth token first
        access_token = self.oauth_client.get_valid_token()
        logger.debug("Obtained OAuth access token")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Construct the payload with PAYER and LABEL_OWNER roles
        payload = {
            "roles": [
                {
                    "roleName": "PAYER",
                    "CRID": "48179940",
                    "MID": "903856638",  # Using Outbound MID
                    "manifestMID": "903856638",  # Using same Outbound MID
                    "accountType": "EPS",
                    "accountNumber": "1000278648"  # EPS Account Number
                },
                {
                    "roleName": "LABEL_OWNER",
                    "CRID": "48179940",
                    "MID": "903856638",  # Using Outbound MID
                    "manifestMID": "903856638",  # Using same Outbound MID
                    "accountType": "EPS",
                    "accountNumber": "1000278648"  # EPS Account Number
                }
            ]
        }

        logger.debug(f"Payment authorization payload: {payload}")

        try:
            logger.debug(f"Making POST request to {self.PAYMENT_AUTH_ENDPOINT}")
            response = requests.post(
                self.PAYMENT_AUTH_ENDPOINT,
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            logger.info("Successfully obtained payment authorization")
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Payment authorization request failed: {str(e)}")
            raise ValueError(f"Failed to obtain payment authorization: {str(e)}")

    def validate_payment_token(self, payment_token: str) -> bool:
        """
        Validate a payment authorization token

        Args:
            payment_token (str): The payment token to validate

        Returns:
            bool: True if the token is valid, False otherwise
        """
        # Implement token validation logic based on API requirements
        pass
