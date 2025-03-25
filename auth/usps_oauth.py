from flask import session
from datetime import datetime, timedelta
from typing import Optional, Dict
import requests
import os
import json
from pathlib import Path


class USPSOAuth2:
    """Manages OAuth2 token storage and retrieval using either Flask sessions or file storage"""

    def __init__(self, token_url: str):
        self.token_url = token_url
        self.session_key = 'usps_oauth'
        # Create a .cache directory in the project root if it doesn't exist
        self.cache_dir = Path(__file__).parent.parent / '.cache'
        self.cache_dir.mkdir(exist_ok=True)
        self.token_file = self.cache_dir / 'usps_token.json'

    def get_stored_token(self) -> Optional[str]:
        """
        Retrieve stored token if it exists and is not expired
        """
        try:
            # Try Flask session first
            if self._has_request_context():
                return self._get_from_session()
            # Fall back to file storage
            return self._get_from_file()
        except Exception:
            return None

    def store_token(self, token_data: Dict) -> None:
        """Store token data in session or file"""
        # Add expiration timestamp (default to 1 hour if not provided)
        expires_in = token_data.get('expires_in', 3600)
        token_data['expires_at'] = (datetime.now() + timedelta(seconds=expires_in)).timestamp()

        if self._has_request_context():
            session[self.session_key] = token_data
        else:
            self._store_in_file(token_data)

    def _has_request_context(self) -> bool:
        """Check if we're in a Flask request context"""
        try:
            from flask import has_request_context
            return has_request_context()
        except Exception:
            return False

    def _get_from_session(self) -> Optional[str]:
        """Get token from Flask session"""
        token_data = session.get(self.session_key)
        if not token_data:
            return None

        if datetime.now().timestamp() > token_data.get('expires_at', 0):
            self.clear_token()
            return None

        return token_data.get('access_token')

    def _get_from_file(self) -> Optional[str]:
        """Get token from file storage"""
        try:
            if not self.token_file.exists():
                return None

            with open(self.token_file, 'r') as f:
                token_data = json.load(f)

            if datetime.now().timestamp() > token_data.get('expires_at', 0):
                self.clear_token()
                return None

            return token_data.get('access_token')
        except Exception:
            return None

    def _store_in_file(self, token_data: Dict) -> None:
        """Store token data in file"""
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)

    def clear_token(self) -> None:
        """Remove token data from both storage methods"""
        if self._has_request_context():
            session.pop(self.session_key, None)

        # Also clear file storage
        if self.token_file.exists():
            self.token_file.unlink()

    def get_new_token(self) -> str:
        """
        Request new token from USPS OAuth2 server

        Returns:
            str: The new access token

        Raises:
            ValueError: If credentials are invalid or missing
        """
        client_id = os.getenv("USPS_CONSUMER_KEY")
        client_secret = os.getenv("USPS_CONSUMER_SECRET")

        if not client_id or not client_secret:
            raise ValueError("Missing USPS credentials in environment variables")

        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": "hatcherybrain.com",
        }

        try:
            response = requests.post(
                self.token_url,
                auth=(client_id, client_secret),
                data=data
            )

            response.raise_for_status()
            token_data = response.json()

            # Store the token data
            self.store_token(token_data)

            return token_data['access_token']

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise ValueError("Invalid USPS credentials")
            else:
                raise e

    def get_valid_token(self) -> str:
        """
        Get a valid token, either from storage or by requesting a new one

        Returns:
            str: A valid access token
        """
        token = self.get_stored_token()
        if token:
            return token

        return self.get_new_token()
