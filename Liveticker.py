# -*- coding: utf-8-*-
import json
import requests
from datetime import date

anzahlTore = 0

def run(self):
    self.timestamp = self.gather(self.timestamp)
    
def handleLiveticker(self, lastDate):
    #merke dir das Team
    team = self.profile["Liveticker"]["Team"]
    #merke dir die Liga
    liga = self.profile["Liveticker"]["Liga"]
    #merke dir die aktuelle Saison
    saison = date.today().year
    if date.today().month < 7:
        saison = saison - 1
    #merke dir den aktuellen Spieltag
    spieltag = json.loads(requests.get("http://www.openligadb.de/api/getcurrentgroup/" + liga).text)["GroupOrderID"]
    
    def getLetzteAenderung(liga, saison, spieltag):
        return json.loads(requests.get(("http://www.openligadb.de/api/getlastchangedate/" +  
                    + liga + "/" + str(saison) + "/" + str(spieltag))).text)
    
    #wenn nichts geupdated wurde, gibt man einfach den alten timestamp zurück
    if lastDate == getLetzteAenderung(liga, saison, spieltag):
        return lastDate

    def getErgebnis(team, liga, spieltag):
        ergebnis = json.loads(requests.get("http://www.openligadb.de/api/getmatchdata/" \
                    + liga + "/" + str(saison) + "/" + str(spieltag)).text)
        for spiel in ergebnis["spiele"]:
            if spiel["Team1"]["TeamName"] == team or spiel["Team2"]["TeamName"] == team:
                return spiel
        return {}
        
    #hole dir das aktuelle Ergebnis des Teams
    ergebnis = getErgebnis(team, liga, saison, spieltag)
    
    #wenn getErgebnis ein leeres dict zurückgibt, gibt man einfach den alten timestamp zurück
    if ergebnis == {}:
        return lastDate
    
    #hole dir das Tore Array
    tore = ergebnis["Goals"]
    
    #wenn ein Tor gefallen ist, pack das Tor in die Queue
    if self.anzahlTore != len(tore):
        lastDate = getLetzteAenderung(liga, saison, spieltag)
        self.anzahlTore = len(tore)
        
        def getLetztesTor(tore):
            tmp = {"GoalID":0}
            for tor in tore:
                if tor["GoalID"] > tmp["GoalID"]:
                    tmp = tor
            return tmp
        #merke dir das zuletzt gefallene Tor
        letztesTor = getLetztesTor(tore)
        
        def formatiereTor(tor):
            heimTeam = ergebnis["Team1"]["TeamName"]
            auswaertsTeam = ergebnis["Team2"]["TeamName"]
            heimTore = tor["ScoreTeam1"]
            auswaertsTore = tor["ScoreTeam2"]
            spielminute = tor["MatchMinute"]
            torschuetze = tor["GoalGetterName"]
            return ("Tor durch " + torschuetze + " in der " + str(spielminute) + ". Spielminute! Neuer Zwischenstand: "
                    + heimTeam + " " + str(heimTore) + " : " + str(auswaertsTore) + " " + auswaertsTeam)
        #packe das neue Tor in die Queue
        if letztesTor["GoalID"] > 0:
            self.q.put(formatiereTor(letztesTor))
            print(formatiereTor(letztesTor))
    
    #wenn das Spiel vorbei ist, setze die Anzahl der Tore zurück
    if ergebnis["MatchIsFinished"]:
        self.anzahlTore = 0
    
    return lastDate
    
self.notifiers = [
    self.NotificationClient(self.handleLiveticker, None)]
