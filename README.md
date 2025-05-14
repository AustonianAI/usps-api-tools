# USPS API Python Tools

A Python application to demonstrate interacting with the USPS APIs.

## Features

- Calculate shipping zones between origin and destination ZIP codes
- Track USPS packages with detailed status information
- Get payment authorization tokens for USPS API access
- Automatic token caching and management for both OAuth and payment tokens

## Prerequisites

- Python 3.8+
- USPS API credentials (requires USPS approval)
- USPS Business Account with appropriate permissions

## USPS API Access

This application uses several USPS APIs that require approval:

1. **Tracking API**: For package tracking functionality
2. **Payments API**: For payment authorization tokens

To get access to these APIs:

1. Create a USPS Business Account through the [USPS Customer Onboarding Portal](https://developers.usps.com/getting-started)
2. Log in to the [USPS Developer Portal](https://developers.usps.com/getting-started)
3. Create an application and select the required API products
4. Retrieve your Consumer Key and Secret
5. Authorize your application to access protected information resources

For more detailed information about the approval process, please visit the [USPS Getting Started Guide](https://developers.usps.com/getting-started).

## Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# USPS API Configuration
USPS_API_BASE_URL=https://apis.usps.com
USPS_API_TEST_URL=https://apis-tem.usps.com

# USPS OAuth Credentials
USPS_CONSUMER_KEY=your_consumer_key
USPS_CONSUMER_SECRET=your_consumer_secret

# USPS Payment Configuration
USPS_PAYMENT_CRID=your_crid
USPS_PAYMENT_MID=your_mid
USPS_PAYMENT_MANIFEST_MID=your_manifest_mid
USPS_PAYMENT_ACCOUNT_TYPE=EPS
USPS_PAYMENT_ACCOUNT_NUMBER=your_account_number

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables
5. Run the application:
   ```bash
   flask run
   ```

## Usage

### Calculate Shipping Zone

```bash
flask zone <origin_zip> <destination_zip>
```

### Track Package

```bash
flask track <tracking_number>
```

### Get Payment Authorization Token

```bash
flask payments
```

Options:

- `--test/--prod`: Use test or production environment (default: test)
- `--output`: Save token to file (optional)

The payment token is automatically cached in `.cache/usps_payments_token.json` and will be reused if valid (tokens expire after 8 hours).

## Project Structure

```
.
├── .cache/                    # Token cache directory
├── auth/                      # Authentication modules
├── payments/                  # Payment-related modules
├── utils/                     # Utility modules
├── app.py                     # Main application
├── config.py                  # Main configuration
├── payments_config.py         # Payment-specific configuration
└── requirements.txt           # Project dependencies
```

## License

[Your License Here]

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
# Track a USPS package
flask track 9400100000000000000000

# The tool will return the tracking information, for example:
# Tracking number: 9400100000000000000000
# Status: Delivered
# Delivery date: 2024-01-01
# Delivery location: 123 Main St, Anytown, USA
# Delivery time: 10:00 AM
```

2. Calculate shipping zone:

```bash
# Calculate shipping zone for origin ZIP code 94016 and destination ZIP code 78701
flask zone 94016 78701

# The tool will return the appropriate zone, for example:
# Zone: 7
```

3. NDC (Network Distribution Center) Lookup

```bash
# Look up NDC for a ZIP code
flask ndc 78701

# The tool will return the appropriate NDC label, for example:
# NDC NEW JERSEY NJ 07097
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

```markdown
├── auth/
│ └── usps_oauth.py # OAuth2 token management
├── data/
│ └── Format2.txt # USPS zone matrix data file
│ └── DMM_L601.csv # USPS NDC data file for NDC lookup
├── utils/
│ ├── tracking.py # USPS tracking functionality
│ └── zone.py # Zone calculation utilities
│ └── ndc.py # NDC lookup utilities
├── .cache/ # Token storage for CLI operations (auto-generated)
├── .env.example # Example environment configuration
├── app.py # Main Flask application with CLI commands
├── requirements.txt # Python package dependencies
├── .gitignore # Git ignore rules
└── README.md # Project documentation
```

The application is organized into several modules:

- `auth/`: Contains OAuth2 authentication handling

  - `usps_oauth.py`: Manages token storage and retrieval for both CLI and web contexts

- `data/`: Contains data files needed for calculations

  - `Format2.txt`: USPS zone matrix data file for zone calculations
  - `DMM_L601.csv`: USPS NDC data file for NDC lookup

- `utils/`: Contains core functionality modules

  - `tracking.py`: USPS tracking API integration
  - `zone.py`: Zone calculation utilities
  - `ndc.py`: NDC lookup utilities

- `.cache/`: Auto-generated directory for storing OAuth tokens in CLI mode
  - `usps_token.json`: Temporary token storage (auto-generated)

Note: The `.cache/` directory and its contents are automatically managed by the application and should not be committed to version control.

## Technical Details

The zone calculation process:

1. `find_zone_row`: Locates the correct row in Format2.txt by matching the first three digits of the origin ZIP code
2. `determine_zone_column`: Calculates the column position using the formula: ((first_three_digits - 1) \* 2) + 4
3. `get_zone_from_row_and_column`: Retrieves the zone value from the intersection of the row and column

Note: The application requires both Format2.txt and DMM_L601.csv to be present in the project /data directory.

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

For detailed information about USPS zone calculations and technical specifications, refer to the [USPS National Zone Charts Matrix Technical Guide](https://postalpro.usps.com/national-zone-charts-matrix/ZoneChartsMatrixTechnicalGuide).

To see the data source for the USPS Network Distribution Center (NDC) lookup, refer to the [USPS Facility Access and Shipment Tracking (FAST) system](https://fast.usps.com/fast/fastApp/resources/labelListFilesSearch.action).
