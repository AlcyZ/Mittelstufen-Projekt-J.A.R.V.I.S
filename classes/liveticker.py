import datetime
import json
import requests

class Liveticker:

    # API Endpunkt von OpenLigaDB für aktuelle Ergebnisse
    API = "http://www.openligadb.de/api/"

    
    def __init__(self, team, liga):
    """
        Initialization of the Liveticker module.
        Initialized properties:
            ::team
            ::liga
            ::saison
            ::spieltag
        """
    self.team = team
    self.liga = liga
    self.saison = getAktuelleSaison()
    self.spieltag = getAktuellerSpieltag()
    

    def getAktuelleSaison():
        """ Merke dir die aktuelle Saison, bis zum Juni läuft die Saison aus dem Vorjahr noch 
                eventuell bessere Methode überlegen, dies funktioniert nur für Bundesliga afaik
        """
        if date.today().month < 7:
            return date.today().year - 1
        return date.today().year
        
    def getAktuellerSpieltag():
        """ Merke dir den aktuellen Spieltag aus der übergebenen Liga """
        return json.loads(requests.get(API + "getcurrentgroup/" + self.liga).text)["GroupOrderID"]

    def getLetzteAenderung():
        """ Hole dir den Timestamp der letzten Änderung vom aktuellen Spieltag 
                Returns: Das date der letzten Änderung vom aktuellen Spieltag
        """
        return json.loads(requests.get((API + "getlastchangedate/" + self.liga + "/" + str(self.saison) + "/" + str(self.spieltag))).text)

    def getErgebnis():
        """ Hole dir das Ergebnis zu den übergebenen Parametern
                Returns: Ein dict mit dem aktuellen Ergebnis zum Spiel des Teams
        """
        response = json.loads(requests.get(API + "getmatchdata/" + self.liga + "/" + str(self.saison) + "/" + str(self.spieltag)).text)
        for spiel in response:
            if getTeam(spiel, 1) == self.team or getTeam(spiel, 2) == self.team:
                return spiel
        return {}
        
    def getTeam(ergebnis, teamNr):
        """ Hole dir den Namen des Teams aus dem Ergebnis dict 
                Returns: Der Name des Teams mit der Teamnummer 1 oder 2
        """
        return ergebnis["Team" + str(teamNr)]["TeamName"]

    def getTore(ergebnis, teamNr):
        """ Hole dir die Anzahl der Tore vom Team aus dem Ergebnis dict 
                Returns: Die Anzahl der Tore des Teams mit der Teamnummer 1 oder 2
        """
        return ergebnis["ScoreTeam" + str(teamNr)]
        
    def getLetztesTor(ergebnis):
        """ Hole dir die maximale GoalID aus dem Goals Array vom Ergebnis 
                Returns: Das dict des letzten geschossenen Tors aus dem Spiel ergebnis
        """
        letztesTor = ["GoalID" : "0"]
        if ergebnis["Goals"]:
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
    