# USPS Shipping Zone Calculator

A Flask application for calculating USPS shipping zones based on origin and destination ZIP codes.

## Setup

1. Clone the repository

```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

The application provides a command-line interface to calculate shipping zones:

```bash
flask calc-zone [origin_zip] [destination_zip]
```

For example:

```bash
flask calc-zone 78701 94016
```

This will:

1. Find the corresponding row in Format2.txt based on the origin ZIP code's first three digits
2. Calculate the appropriate column based on the destination ZIP code's first three digits
3. Return the shipping zone for that origin-destination pair

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
