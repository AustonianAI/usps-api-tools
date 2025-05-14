from typing import Dict, Optional
from datetime import datetime, timedelta
import requests
import logging
import json
from pathlib import Path
from auth.usps_oauth import USPSOAuth2
from config import get_payments_url
from payments_config import get_payment_payload

# Configure logging for the payments module
logger = logging.getLogger(__name__)


class USPSPayments:
    """Handles USPS payment operations including authorization and token management"""

    def __init__(self, use_test: bool = True):
        """Initialize the payments client with its own OAuth manager"""
        logger.info("Initializing USPS Payments client")
        self.oauth_client = USPSOAuth2(use_test)
        self.payment_auth_endpoint = f"{get_payments_url(use_test)}/payment-authorization"

        # Set up cache directory and token file
        self.cache_dir = Path(__file__).parent.parent / '.cache'
        self.cache_dir.mkdir(exist_ok=True)
        self.token_file = self.cache_dir / 'usps_payments_token.json'
        logger.info(f"Payment token will be stored at: {self.token_file}")

    def get_stored_payment_token(self) -> Optional[Dict]:
        """
        Retrieve stored payment token if it exists and is not expired
        """
        try:
            if not self.token_file.exists():
                logger.debug("Payment token file does not exist")
                return None

            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
                logger.debug(f"Read payment token data from file: {self.token_file}")

            # Check if token is expired (8 hours from issuance)
            if datetime.now().timestamp() > token_data.get('expires_at', 0):
                logger.debug("Payment token has expired")
                self.clear_payment_token()
                return None

            logger.debug("Retrieved valid payment token from file")
            return token_data
        except Exception as e:
            logger.error(f"Error retrieving payment token: {str(e)}")
            return None

    def store_payment_token(self, token_data: Dict) -> None:
        """Store payment token data in file"""
        try:
            # Add expiration timestamp (8 hours from issuance)
            token_data['expires_at'] = (datetime.now() + timedelta(hours=8)).timestamp()
            logger.debug(f"Storing payment token with expiration: {datetime.fromtimestamp(token_data['expires_at'])}")

            with open(self.token_file, 'w') as f:
                json.dump(token_data, f)
            logger.debug(f"Successfully stored payment token in file: {self.token_file}")
        except Exception as e:
            logger.error(f"Error storing payment token: {str(e)}")
            raise

    def clear_payment_token(self) -> None:
        """Remove payment token data from storage"""
        try:
            if self.token_file.exists():
                logger.debug(f"Removing payment token file: {self.token_file}")
                self.token_file.unlink()
        except Exception as e:
            logger.error(f"Error clearing payment token: {str(e)}")

    def get_payment_authorization(self) -> Dict:
        """
        Obtain a payment authorization token from USPS

        Returns:
            Dict: Payment authorization response containing the token and other details

        Raises:
            ValueError: If the request fails or returns an error
        """
        logger.info("Requesting payment authorization token")

        # Try to get existing token first
        stored_token = self.get_stored_payment_token()
        if stored_token:
            logger.info("Using stored payment token")
            return stored_token

        # Get a valid OAuth token first
        access_token = self.oauth_client.get_valid_token()
        logger.debug("Obtained OAuth access token")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Get the payload from config
        payload = get_payment_payload()
        logger.debug("Using payment payload from configuration")

        try:
            logger.debug(f"Making POST request to {self.payment_auth_endpoint}")
            response = requests.post(
                self.payment_auth_endpoint,
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            token_data = response.json()
            logger.info("Successfully obtained payment authorization")

            # Store the token data
            self.store_payment_token(token_data)

            return token_data

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
