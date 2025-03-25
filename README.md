# USPS Tools and API Integrations

This Flask application provides integration with the USPS Tracking API v3, allowing you to track packages and calculate shipping zones.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/AustonianAI/usps-api-tools
   cd usps-api-tools
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and fill in your USPS API credentials:

   ```bash
   nano .env  # or use your preferred editor
   ```

   Required environment variables:

   - `USPS_CONSUMER_KEY`: Your USPS API consumer key
   - `USPS_CONSUMER_SECRET`: Your USPS API consumer secret

## Authentication

The application uses OAuth2 for USPS API authentication with a hybrid storage system:

- **CLI Commands**: Tokens are stored in `.cache/usps_token.json`
- **Web Requests**: Tokens are stored in Flask sessions (no HTTP requests are implemented yet, just CLI commands)

Token management features:

- Automatic token refresh when expired
- Secure storage in both web and CLI contexts
- Automatic retry on authentication failures

## Usage

### CLI Commands

1. Track a USPS package:

```bash
flask track 9400100000000000000000
```

2. Calculate shipping zone:

```bash
flask zone 94016 78701
```

## Token Storage

### Web Sessions

- Tokens for web requests are stored in Flask sessions
- Secured by `FLASK_SECRET_KEY`
- Automatically handled per user session

### CLI Cache

- CLI tokens stored in `.cache/usps_token.json`
- Cache directory is automatically created
- Tokens include expiration timestamps
- Cache is automatically cleared when tokens expire

## Security Notes

1. Never commit:

   - `.env` file with real credentials
   - `.cache` directory contents
   - `FLASK_SECRET_KEY`

2. In production:
   - Use a strong `FLASK_SECRET_KEY`
   - Secure the `.cache` directory permissions
   - Use environment variables for all sensitive data

## Development

The application uses:

- Flask for web framework
- Click for CLI commands
- Requests for API communication
- OAuth2 for USPS authentication

## Error Handling

The application includes:

- Token expiration handling
- Automatic token refresh
- Invalid credential detection
- API error handling
- Retry logic for failed requests

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[MIT License](LICENSE)

Be excellent to each other.

## Project Structure

├── auth/
│ └── usps_oauth.py # OAuth2 token management
├── data/
│ └── Format2.txt # USPS zone matrix data file
├── utils/
│ ├── tracking.py # USPS tracking functionality
│ └── zone.py # Zone calculation utilities
├── .cache/ # Token storage for CLI operations (auto-generated)
├── .env.example # Example environment configuration
├── app.py # Main Flask application with CLI commands
├── requirements.txt # Python package dependencies
├── .gitignore # Git ignore rules
└── README.md # Project documentation

The application is organized into several modules:

- `auth/`: Contains OAuth2 authentication handling

  - `usps_oauth.py`: Manages token storage and retrieval for both CLI and web contexts

- `data/`: Contains data files needed for calculations

  - `Format2.txt`: USPS zone matrix data file for zone calculations

- `utils/`: Contains core functionality modules

  - `tracking.py`: USPS tracking API integration
  - `zone.py`: Zone calculation utilities
  - `__init__.py`: Package initialization

- `.cache/`: Auto-generated directory for storing OAuth tokens in CLI mode
  - `usps_token.json`: Temporary token storage (auto-generated)

Note: The `.cache/` directory and its contents are automatically managed by the application and should not be committed to version control.

## Technical Details

The zone calculation process:

1. `find_zone_row`: Locates the correct row in Format2.txt by matching the first three digits of the origin ZIP code
2. `determine_zone_column`: Calculates the column position using the formula: ((first_three_digits - 1) \* 2) + 4
3. `get_zone_from_row_and_column`: Retrieves the zone value from the intersection of the row and column

Note: The application requires Format2.txt to be present in the project root directory. This file contains the USPS zone matrix data.

## Future Development

Planned enhancements include:

- Military ZIP code handling:
  - Special zone calculations for APO/FPO/DPO addresses
  - Support for military ZIP codes (340XX, 961XX, etc.)
- NDC (Network Distribution Center) features:
  - NDC Entry Discount indicators
  - NDC facility lookup and validation
- Web interface for zone lookups
- Postage rate calculations
- Support for different mail classes
- API endpoints for integration with other systems

## References

For detailed information about USPS zone calculations and technical specifications, refer to the [USPS National Zone Charts Matrix Technical Guide](https://postalpro.usps.com/national-zone-charts-matrix/ZoneChartsMatrixTechnicalGuide)
