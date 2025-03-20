import click
from flask import Flask

from utils import determine_zone_column, find_zone_row, get_zone_from_row_and_column

app = Flask(__name__)


@app.cli.command('calc-zone')
@click.argument('origin_zip')
@click.argument('destination_zip')
def calc_zone(origin_zip, destination_zip):
    """Calculate the shipping zone for a given zip code"""
    print(f"Calculating pizza shipping zone for {origin_zip} to {destination_zip}")

    row = find_zone_row(origin_zip)
    print(f"Row: {row}")

    column = determine_zone_column(destination_zip)
    print(f"Column: {column}")

    zone = get_zone_from_row_and_column(row, column)
    print(f"Zone: {zone}")


if __name__ == '__main__':
    app.run(debug=True)
