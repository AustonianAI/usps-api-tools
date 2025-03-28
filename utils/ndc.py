import csv
from typing import Optional


def parse_zip_range(zip_range: str) -> set[int]:
    """
    Parse a zip code range string (e.g. "240-241, 243, 245, 270-278") 
    into a set of individual 3-digit zip codes.
    """
    zip_codes = set()

    # Split by comma and process each part
    parts = [p.strip() for p in zip_range.split(',')]

    for part in parts:
        if '-' in part:
            # Handle range (e.g. "240-241")
            start, end = map(int, part.split('-'))
            zip_codes.update(range(start, end + 1))
        else:
            # Handle individual zip code
            zip_codes.add(int(part))

    return zip_codes


def get_ndc_label(zip_code: str) -> Optional[str]:
    """
    Find the NDC label for a given ZIP code.

    Args:
        zip_code: A ZIP code string (e.g. "24060", "08234", "082", "00123-4567")

    Returns:
        The corresponding NDC label or None if not found
    """
    # Clean up the zip code and get first 3 digits
    cleaned_zip = zip_code.strip().replace('-', '')[:3]

    try:
        # Convert to integer for comparison
        zip_int = int(cleaned_zip)
    except ValueError:
        print(f"Invalid ZIP code format: {zip_code}")
        return None

    with open('data/DMM_L601.csv', 'r') as f:
        reader = csv.reader(f)

        # Find the header row
        for row in reader:
            if row and row[0].strip() == 'Column A Destination ZIP Codes':
                # Found the header row, now we can process the data
                break

        # Process the actual data rows
        for row in reader:
            if not row:  # Skip empty rows
                continue

            zip_range = row[0].strip()
            label = row[1].strip()

            # Parse the zip range and check if our zip code is in it
            valid_zips = parse_zip_range(zip_range)
            if zip_int in valid_zips:
                return label

    return None
