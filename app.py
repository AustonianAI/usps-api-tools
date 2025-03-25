import click
from flask import Flask, json


import utils.tracking as tracking
import utils.zone as zone

app = Flask(__name__)


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

    data = tracking.get_usps_access_token()

    access_token = data['access_token']

    tracking_data = tracking.track_usps_package(tracking_number, access_token, "DETAIL")

    print(json.dumps(tracking_data, indent=4))


if __name__ == '__main__':
    app.run(debug=True)
