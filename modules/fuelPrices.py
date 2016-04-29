# -*- coding: utf-8 -*-

"""
Retrieve the current
average fuel prices for E5, E10 and Diesel.
"""

import re
from classes.fuelPrices import FuelPrices

WORDS = ["FUEL"]

def isValid(text):
    """Validate the call of this module.""""
    return bool(re.search(r'\bfuel\b', text, re.IGNORECASE))
    
def handle(text, mic, profile):
    "Get fuel prices and answer to customer."
    
    fuelPrices = FuelPrices()
    
    mic.say("Getting the fuel prices. Hold on please.")
    
    try:
        prices = fuelPrices.get_prices()
        mix.say("The current average fuel prices are")
        mic.say("E5:" + prices.e5)
        mic.say("E10:" + prices.e10)
        mic.say("Diesel:" + prices.diesel)
        break
    except Exception:
        mic.say("Sorry, there was an error while retrieving the prices.")
     