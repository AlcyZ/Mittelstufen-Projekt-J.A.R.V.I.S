import re
import subprocess
from client import jasperpath

WORDS = ["RADIO"]

def handle(text, mic, profile):
    """
        plays internet radio
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    befehle = ["STOP", "PLAY", "NEXT", "PREVIOUS", "VOLUME", "UP", "DOWN", "EXIT"]
    music_stt_engine = mic.active_stt_engine.get_instance("music", befehle)
    
    mic.say("Starting radio . . .")
    
    # Liest die gespeicherten Playlists aus einer Textdatei aus
    def get_playlists(filename=jasperpath.data('text', 'playlists.txt'):
        pl_file = open(filename, "r")
        playlists = []
        for line in pl_file.readlines():
            line = line.replace("\n", "")
            playlists.append(line)
        return playlists
    
    index = 0
    playlists = get_playlists()
    if len(playlists) = 0:
        mic.say("You don't have any playlists in your playlist file!")
        return
    
    # TODO: Datei ~/.mpdconf anpassen: http://www.musicpd.org/doc/user/
    # kann eventuell auch in den Autostart?
    subprocess.call("mpd")
    
    # erste playlist laden und abspielen
    MPD.load(playlists[0])
    MPD.play()
    
    cmd = ""    
    while (cmd != "EXIT"):
        cmd = mic.passivelisten().upper()
        if cmd in befehle:
            if cmd = "PLAY": # play
                MPD.play()
            elif cmd = "STOP": # stop
                MPD.stop()
            elif cmd = "VOLUME": # lautstaerke
                cmd = mic.activeListen().upper()
                if cmd = "UP":
                    MPD.vol_up()
                elif cmd = "DOWN":
                    MPD.vol_down()
            elif cmd = "NEXT": # naechste playlist
                MPD.stop()
                index += 1
                if index > len(playlists) - 1:
                    index = 0
                MPD.load(playlists[index])
                MPD.play()
            elif cmd = "PREVIOUS": # vorherige playlist
                MPD.stop()
                index -= 1
                if index < 0:
                    index = len(playlists) - 1
                MPD.load(playlists[index])
                MPD.play()
    MPD.stop()

def isValid(text):
    """
        Returns True if input is related to the radio.
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bradio\b', text, re.IGNORECASE))
    
class MPD(object):

    @staticmethod
    def load(self, playlist):
        subprocess.call("mpc load " + playlist, shell=True)

    @staticmethod
    def play(self):
        subprocess.call("mpc play", shell=True)
        
    @staticmethod
    def stop(self):
        subprocess.call("mpc stop" shell=True)
        
    @staticmethod
    def vol_up(self):
        subprocess.call("mpc volume +10", shell=True)
        
    @staticmethod
    def vol_down(self):
        subprocess.call("mpc volume -10", shell=True)
        
    @staticmethod
    def next(self): # nicht benutzt
        subprocess.call("mpc next", shell=True)
        
    @staticmethod
    def previous(self): # nicht benutzt
        subprocess.call("mpc previous", shell=True)
