import requests
import os
from typing import Dict, Optional

from auth.usps_oauth import USPSOAuth2

# Create a global sewssion manager instance
oauth_manager = USPSOAuth2("https://apis.usps.com/oauth2/v3/token")


def track_usps_package(tracking_number: str, expand: str = "SUMMARY") -> Dict:
    """
    Track a USPS package using the USPS API v3.

    Args:
        tracking_number (str): The USPS tracking number to look up
        expand (str, optional): Level of detail to return. Either "SUMMARY" or "DETAIL". 
        Defaults to "SUMMARY".

    Returns:
        Dict: The tracking information response from USPS

    Raises:
        requests.exceptions.RequestException: If the API request fails
        ValueError: If the tracking number is invalid or not found
    """
    base_url = "https://apis.usps.com/tracking/v3"
    endpoint = f"/tracking/{tracking_number}"

    # Get a valid token using the session manager
    access_token = oauth_manager.get_valid_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
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

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(f"Tracking number {tracking_number} not found")
        elif response.status_code == 401:
            # Clear the invalid token and retry once
            oauth_manager.clear_token()
            access_token = oauth_manager.get_valid_token()

            # Retry with new token
            headers["Authorization"] = f"Bearer {access_token}"
            response = requests.get(
                base_url + endpoint,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        else:
            raise e
