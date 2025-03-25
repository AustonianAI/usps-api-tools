import requests
import os
from typing import Dict, Optional


def get_usps_access_token() -> str:
    """
    Get an OAuth2 access token from USPS using client credentials flow.

    Returns:
        str: The access token

    Raises:
        requests.exceptions.RequestException: If the token request fails
        ValueError: If credentials are invalid
    """
    token_url = "https://api.usps.com/oauth2/v3/token"

    # Get credentials from environment variables
    client_id = os.getenv("USPS_CONSUMER_KEY")
    client_secret = os.getenv("USPS_CONSUMER_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Missing USPS credentials in environment variables")

    # Request body for client credentials flow
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "hatcherybrain.com",
    }

    try:
        response = requests.post(
            token_url,
            auth=(client_id, client_secret),
            data=data
        )

        response.raise_for_status()
        token_data = response.json()

        return token_data

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise ValueError("Invalid USPS credentials")
        else:
            raise e


def track_usps_package(tracking_number: str, api_key: str, expand: str = "SUMMARY") -> Dict:
    """
    Track a USPS package using the USPS API v3.

    Args:
        tracking_number (str): The USPS tracking number to look up
        api_key (str): Your USPS API OAuth token
        expand (str, optional): Level of detail to return. Either "SUMMARY" or "DETAIL". Defaults to "SUMMARY".

    Returns:
        Dict: The tracking information response from USPS

    Raises:
        requests.exceptions.RequestException: If the API request fails
        ValueError: If the tracking number is invalid or not found
    """
    base_url = "https://api.usps.com/tracking/v3"
    endpoint = f"/tracking/{tracking_number}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    params = {
        "expand": expand
    }

    try:
        response = requests.get(
            base_url + endpoint,
            headers=headers,
            params=params
        )

        # Raise an error for bad status codes
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(f"Tracking number {tracking_number} not found")
        elif response.status_code == 401:
            raise ValueError("Invalid API key")
        else:
            raise e
