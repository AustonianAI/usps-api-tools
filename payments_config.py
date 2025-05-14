import os
from typing import Dict

# Payment Configuration
PAYMENT_CONFIG = {
    'crid': os.getenv('USPS_PAYMENT_CRID'),
    'mid': os.getenv('USPS_PAYMENT_MID'),
    'manifest_mid': os.getenv('USPS_PAYMENT_MANIFEST_MID'),
    'account_type': os.getenv('USPS_PAYMENT_ACCOUNT_TYPE', 'EPS'),
    'account_number': os.getenv('USPS_PAYMENT_ACCOUNT_NUMBER'),
}


def get_payment_payload() -> Dict:
    """
    Get the payment authorization payload with environment variables.

    Returns:
        Dict: The payment authorization payload

    Raises:
        ValueError: If required environment variables are missing
    """
    required_vars = ['USPS_PAYMENT_CRID', 'USPS_PAYMENT_MID',
                     'USPS_PAYMENT_MANIFEST_MID', 'USPS_PAYMENT_ACCOUNT_NUMBER']

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return {
        "roles": [
            {
                "roleName": "PAYER",
                "CRID": PAYMENT_CONFIG['crid'],
                "MID": PAYMENT_CONFIG['mid'],
                "manifestMID": PAYMENT_CONFIG['manifest_mid'],
                "accountType": PAYMENT_CONFIG['account_type'],
                "accountNumber": PAYMENT_CONFIG['account_number']
            },
            {
                "roleName": "LABEL_OWNER",
                "CRID": PAYMENT_CONFIG['crid'],
                "MID": PAYMENT_CONFIG['mid'],
                "manifestMID": PAYMENT_CONFIG['manifest_mid']
            },
            {
                "roleName": "RATE_HOLDER",
                "CRID": PAYMENT_CONFIG['crid'],
                "accountType": PAYMENT_CONFIG['account_type'],
                "accountNumber": PAYMENT_CONFIG['account_number']
            }
        ]
    }
