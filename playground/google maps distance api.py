import json
import requests

API = "https://maps.googleapis.com/maps/api/distancematrix/json?"

Start = raw_input("Geben Sie den Startpunkt ein: ")
Ziel  = raw_input("Geben Sie den Zielort ein: ")

response = json.loads(requests.get(API + "origins=" + Start + "&destinations=" + Ziel).text)

if response:
    if response["status"] == "OK":
        Distanz = response["rows"][0]["elements"][0]["distance"]["value"]
        print("Distanz zwischen " + Start + " und " + Ziel + ": " + str(Distanz) + " Meter.")
    else:
        print("Fehlerhafter Status: " + response["status"])
else:
    print("keine Antwort von der Google Maps API")
    
#TODO: äöü usw abfangen und URL-encoden, Leerzeichen durch + ersetzen