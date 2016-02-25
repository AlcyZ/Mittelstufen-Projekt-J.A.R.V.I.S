# -*- coding: utf-8-*-
import requests
import json
import urllib

API_KEY = "DBPLX1HKCWEN8W6MW" #Mein persönlicher API-KEY, für das Projekt einen neuen anfordern?
#VERZEICHNIS ANPASSEN
PLAYLIST_FILE = "E:\\Programmierung\\Python\\PlaylistGenerator\\Playlists\\" #Verzeichnis in dem die Playlists gespeichert werden
ECHO_NEST = "http://developer.echonest.com/api/v4/playlist/static?api_key=" + API_KEY + "&type=genre-radio"
#Gibt noch andere Playlisttypen, z.B. Artist-Radio, Artist-Description oder Song-Radio
#Siehe http://developer.echonest.com/docs/v4/standard.html#static

def main():
    genre = urllib.quote_plus(raw_input("Geben Sie ein Genre ein: "))
    results = raw_input("Geben Sie die Anzahl der Songs ein: ")
    outputFile = PLAYLIST_FILE + genre + "-" + str(results) + ".txt"
    request = ECHO_NEST + "&genre=" + genre + "&results=" + str(results)
    response = requests.get(request)
    playlist = json.loads(response.text)
    if playlist["response"]["status"]["code"] != 0:
        print(str(playlist["response"]["status"]["message"]))
        return
    print("")
    output = ""
    for song in playlist["response"]["songs"]:
        #Der ganze Unicode und UTF-8 Kram ist für Interpreten wie z.B. Tiësto, also Sonderzeichen
        print(unicode(song["artist_name"].encode("utf-8"), encoding="utf-8") + "  -  " + unicode(song["title"].encode("utf-8"), encoding="utf-8"))
        output = output + unicode(song["artist_name"].encode("utf-8"), encoding="utf-8") + "  -  " + unicode(song["title"].encode("utf-8"), encoding="utf-8") + "\n"
        #Hier kann man auch über song["id"] auf die SONG-ID zugreifen und mit SPOTIFY verbinden.
    open(outputFile, "w").write(output.encode("utf-8"))
    
main()