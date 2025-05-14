import os
from typing import Dict

# USPS API Configuration
USPS_API_CONFIG = {
    'base_url': os.getenv('USPS_API_BASE_URL', 'https://apis.usps.com'),
    'test_url': os.getenv('USPS_API_TEST_URL', 'https://apis-tem.usps.com'),
}

# API Version paths
API_VERSIONS = {
    'oauth': '/oauth2/v3',
    'tracking': '/tracking/v3',
    'payments': '/payments/v3',
}


def get_api_url(service: str, use_test: bool = False) -> str:
    """
    Get the full API URL for a specific service.

    Args:
        service (str): The service name (e.g., 'oauth', 'tracking', 'payments')
        use_test (bool): Whether to use the test environment URL

    Returns:
        str: The complete API URL
    """
    base = USPS_API_CONFIG['test_url'] if use_test else USPS_API_CONFIG['base_url']
    version = API_VERSIONS.get(service)
    if not version:
        raise ValueError(f"Unknown service: {service}")
    return f"{base}{version}"

# Convenience functions for common endpoints


def get_oauth_url(use_test: bool = False) -> str:
    return f"{get_api_url('oauth', use_test)}/token"


def get_tracking_url(use_test: bool = False) -> str:
    return get_api_url('tracking', use_test)


def get_payments_url(use_test: bool = False) -> str:
    return get_api_url('payments', use_test)
