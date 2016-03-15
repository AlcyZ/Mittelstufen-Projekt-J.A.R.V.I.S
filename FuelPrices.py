#!/usr/bin/env python
# coding=utf-8

# This script will retrieve the current average
# fuel prices in Germany using the data provided
# by spritpreiskontrolle.de.

import requests

# Class representing a fuel prices getter.
class FuelPrices():

    # API URL.
    API_URL = 'http://data.spritpreiskontrolle.de/api/avgpricetrend.json'

    # Retrieves the average fuel prices.
    def get_prices(self):
        # Perform request.
        response = requests.get(self.API_URL)

        # Check status code and parse or throw exception.
        if response.status_code == 200:
            self.parse_response(response)
        else:
            raise Error('Unexpected server response')

    # Parses the server response.
    def parse_response(self, response):
        # Response as JSON.
        data = response.json()['response']

        # Average prices.
        prices = {
            'e5': data['E5']['price'],
            'e10': data['E10']['price'],
            'diesel': data['Diesel']['price']
        }

        # Output.
        self.output(prices)

    # Outputs prices.
    def output(self, prices):
        print '======================='
        print '  AVERAGE FUEL PRICES  '
        print '======================='
        print ''
        print 'Petrol E5: ' + str(prices['e5'])
        print 'Petrol E10: ' + str(prices['e10'])
        print 'Diesel: ' + str(prices['diesel'])

fuelPrices = FuelPrices()
fuelPrices.get_prices()
