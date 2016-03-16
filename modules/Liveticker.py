# -*- coding: utf-8-*-
import json
import requests

from datetime import date

WORDS = ["LIVETICKER"]

def getAktuelleSaison():
    """ Merke dir die aktuelle Saison, bis zum Juni läuft die Saison aus dem Vorjahr noch """
    if date.today().month < 7:
        return date.today().year - 1
    return date.today().year
    
def getAktuellerSpieltag(liga):
    """ Merke dir den aktuellen Spieltag aus der übergebenen Liga """
    return json.loads(requests.get("http://www.openligadb.de/api/getcurrentgroup/" + liga).text)["GroupOrderID"]

def getLetzteAenderung(liga, saison, spieltag):
    """ Hole dir den Timestamp der letzten Änderung vom aktuellen Spieltag """
    return json.loads(requests.get(("http://www.openligadb.de/api/getlastchangedate/" + liga + "/" + str(saison) + "/" + str(spieltag))).text)

def getErgebnis(team, liga, saison, spieltag):
    """ Hole dir das Ergebnis zu den übergebenen Parametern
            Returns: Ein dict mit dem aktuellen Ergebnis zu dem Spiel mit den Parametern
    """
    ergebnis = json.loads(requests.get("http://www.openligadb.de/api/getmatchdata/" + liga + "/" + str(saison) + "/" + str(spieltag)).text)
    for spiel in ergebnis["spiele"]:
        if getTeam(spiel, 1) == team or getTeam(spiel, 2) == team:
            return spiel
    return {}
    
def getTeam(ergebnis, teamNr):
    """ Hole dir den Namen des Teams aus dem Ergebnis dict """
    return ergebnis["Team" + str(teamNr)]["TeamName"]

def getTore(ergebnis, teamNr):
    """ Hole dir die Anzahl der Tore vom Team aus dem Ergebnis dict """
    return ergebnis["ScoreTeam" + str(teamNr)]
    
def getLetztesTor(ergebnis):
    """ Hole dir die maximal GoalID aus dem Goals Array vom Ergebnis """
    letztesTor = ["GoalID" : "0"]
    for goal in ergebnis["Goals"]:
        if goal["GoalID"] > letztesTor["GoalID"]:
            letztesTor = goal
    return letztesTor
    
def formatiereTor(tor):
    """ Formatiere ein dict mit der Form:
            Team1
                TeamName
            Team2
                TeamName
            ScoreTeam1
            ScoreTeam2
            MatchMinute
            GoalGetterName
        
        Returns: den formatierten String
    """
    heimTeam = ergebnis["Team1"]["TeamName"]
    auswaertsTeam = ergebnis["Team2"]["TeamName"]
    heimTore = tor["ScoreTeam1"]
    auswaertsTore = tor["ScoreTeam2"]
    spielminute = tor["MatchMinute"]
    torschuetze = tor["GoalGetterName"]
    return ("Tor durch " + torschuetze + " in der " + str(spielminute) + ". Spielminute! Neuer Zwischenstand: "
            + heimTeam + " " + str(heimTore) + " : " + str(auswaertsTore) + " " + auswaertsTeam)

def handle(text, mic, profile):
    """ Gib den aktuellen Zwischenstand aus dem Spiel des unterstützten Teams zurück.
    """
    if "Liveticker" in profile:
        if "Team" in profile["Liveticker"] and "Liga" in profile["Liveticker"]:
            #merke dir das Team
            team = self.profile["Liveticker"]["Team"]
            #merke dir die Liga
            liga = self.profile["Liveticker"]["Liga"]
            
            ergebnis = getErgebnis(team, liga, getAktuelleSaison(), getAktuellerSpieltag(liga))
            if ergebnis:
                heimTeam = getTeam(ergebnis, 1)
                auswaertsTeam = getTeam(ergebnis, 2)
                heimTore = getTore(ergebnis, 1)
                auswaertsTore = getTore(ergebnis, 2)
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
        mic.say("Sie müssen einen Eintrag in der Profildatei mit dem Namen Liveticker machen!")
        
def isValid(text):
    """ Gib True zurück wenn der Input was mit Liveticker zu tun hat """
    return bool(re.search(r'\bliveticker\b', text, re.IGNORECASE))