# -*- coding: utf-8-*-
import json
import requests

from classes.liveticker import Liveticker
from datetime import date

# expected words to start the module
WORDS = ["LIVETICKER"]

def handle(text, mic, profile):
    """ Gib den aktuellen Zwischenstand aus dem Spiel des unterstützten Teams zurück.
    """
    if "Liveticker" in profile:
        if "Team" in profile["Liveticker"] and "Liga" in profile["Liveticker"]:
            #merke dir das Team
            team = profile["Liveticker"]["Team"]
            #merke dir die Liga
            liga = profile["Liveticker"]["Liga"]
            
            lt = Liveticker(team, liga)
            
            ergebnis = lt.getErgebnis()
            
            if ergebnis:
                heimTeam = Liveticker.getTeam(ergebnis, 1)
                auswaertsTeam = Liveticker.getTeam(ergebnis, 2)
                heimTore = Liveticker.getTore(ergebnis, 1)
                auswaertsTore = Liveticker.getTore(ergebnis, 2)
                if ergebnis["MatchIsFinished"]:
                    output = "Das Endergebnis aus dem Spiel %s gegen %s lautet... %s zu %s." % (heimTeam, auswaertsTeam, heimTore, auswaertsTore)
                else:
                    output = "Der aktuelle Zwischenstand aus dem Spiel %s gegen %s lautet... %s zu %s." % (heimTeam, auswaertsTeam, heimTore, auswaertsTore)
                mic.say(output)
            else:
                mic.say("Fehler beim Auslesen vom Ergebnis. Bitte überprüfen Sie ihre Profildatei und geben Sie richtige Werte für ihr Team und die Liga ein!")
        else:
            mic.say("Sie müssen Angaben zu dem Team und der Liga des Teams in der Profildatei machen! Zum Beispiel 'Werder Bremen' und 'bl1' für die erste Bundesliga.")
    else:
        mic.say("Sie müssen einen Eintrag in der Profildatei mit dem Namen Liveticker haben!")
        
def isValid(text):
    """ Gib True zurück wenn der Input was mit Liveticker zu tun hat """
    return bool(re.search(r'\bliveticker\b', text, re.IGNORECASE))