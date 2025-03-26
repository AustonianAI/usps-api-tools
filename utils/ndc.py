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
    Find the NDC label for a given 3-digit ZIP code.

    Args:
        zip_code: A 3-digit ZIP code string (e.g. "240" or "082")

    Returns:
        The corresponding NDC label or None if not found
    """
    # Convert input to integer for comparison
    zip_int = int(zip_code)

    with open('data/DMM_L601.csv', 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            zip_range = row['Column A Destination ZIP Codes'].strip()
            label = row['Column B Label To'].strip()

            # Parse the zip range and check if our zip code is in it
            valid_zips = parse_zip_range(zip_range)
            if zip_int in valid_zips:
                return label

    return None
