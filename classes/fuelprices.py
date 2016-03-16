#!/usr/bin/env python
# coding=utf-8

import requests


class FuelPrices(object):
    """This class retrieves the current average fuel prices.

    fuel prices in Germany using the data provided
    by spritpreiskontrolle.de.
    """

    API_URL = 'http://data.spritpreiskontrolle.de/api/avgpricetrend.json'

    def get_prices(self):
        """Retrieve the average fuel prices.

        Returns:
            {Object}

        Raises:
            {Error}
        """
        response = requests.get(self.API_URL)

        if response.status_code == 200:
            return self._parse_response(response)
        else:
            raise Exception('Unexpected server response')

    def _parse_response(self, response):
        """Parse the server response.

        Arguments:
            response {Object} -- Server response.

        Returns:
            {Object} -- Fuel prices object.
        """
        data = response.json()['response']

        prices = {
            'e5': data['E5']['price'],
            'e10': data['E10']['price'],
            'diesel': data['Diesel']['price']
        }

        return prices
