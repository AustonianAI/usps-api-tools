# USPS Tools and API Integrations

This Flask application provides integration with the USPS Tracking API v3, allowing you to track packages and calculate shipping zones.

## Setup

1. Clone the repository:

   ```bash
   git clone [your-repository-url]
   cd [repository-name]
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

## Usage

### Track a Package

Use the Flask CLI command to track a package:

```bash
flask tracking-number [tracking-number]
```

This will:

- Authenticate with the USPS API
- Retrieve tracking information
- Save the data to `tracking_data.json`

### Calculate Shipping Zone

Calculate the shipping zone between two ZIP codes:

```bash
flask calc-zone [origin_zip] [destination_zip]
```

## Development

The application uses OAuth2 for authentication with the USPS API.

## Security Notes

- Never commit your `.env` file
- Keep your USPS API credentials secure
- Always use HTTPS in production

## Project Structure

```
.
├── app.py          # Main Flask application with CLI commands
├── utils.py        # Utility functions for zone calculations
├── Format2.txt     # USPS zone matrix data file
├── requirements.txt
├── .gitignore
└── README.md
```

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
