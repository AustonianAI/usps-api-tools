import click
from flask import Flask, json
import os
import logging

import utils.tracking as tracking
import utils.zone as zone
import utils.ndc as ndc
from payments import USPSPayments

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = os.getenv("FLASK_SECRET_KEY", "secret-dev-key")

# Configure Flask logging
app.logger.setLevel(logging.DEBUG)


@app.cli.command("ndc")
@click.argument("zip_code")
def lookup_ndc(zip_code):
    """Get the NDC for a given zip code"""

    ndc_label = ndc.get_ndc_label(zip_code)
    print(f"NDC for {zip_code}: {ndc_label}")


@app.cli.command('zone')
@click.argument('origin_zip')
@click.argument('destination_zip')
def calc_zone(origin_zip, destination_zip):
    """Calculate the shipping zone for a given zip code"""

    row = zone.find_zone_row(origin_zip)

    column = zone.determine_zone_column(destination_zip)

    result = zone.get_zone_from_row_and_column(row, column)
    print(f"Zone: {result}")


@app.cli.command('track')
@click.argument('tracking_number')
def tracking_number(tracking_number):
    """Get the tracking number for a given tracking number"""
    print(f"Tracking number: {tracking_number}")

    tracking_data = tracking.track_usps_package(tracking_number, "DETAIL")
    print(json.dumps(tracking_data, indent=4))


@app.cli.command('payments')
@click.option('--test/--prod', default=True, help='Use test environment (default) or production')
@click.option('--output', type=click.Path(), help='Save token to file (optional)')
def payments(test, output):
    """Get a USPS payment authorization token"""
    try:
        # Initialize payments client
        payments_client = USPSPayments(use_test=test)

        # Get payment authorization
        result = payments_client.get_payment_authorization()

        # Print the token
        click.echo("\nPayment Authorization Token:")
        click.echo("-" * 50)
        click.echo(result['paymentAuthorizationToken'])
        click.echo("\nFull Response:")
        click.echo("-" * 50)
        click.echo(json.dumps(result, indent=2))

        # Save to file if output path provided
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"\nToken saved to {output}")

    except Exception as e:
        click.echo(f"Error getting payment token: {str(e)}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    app.run(debug=True)
