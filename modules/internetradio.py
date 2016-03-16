import re
import subprocess
from client import jasperpath

WORDS = ["RADIO"]


def handle(text, mic, profile):
    """Play internet radio.

    Arguments:
        text {string} -- user-input, typically transcribed speech
        mic {object} -- used to interact with the user (for both input and output)
        profile {object} -- contains information related to the user (e.g., phone
                            number)
    """
    mic.say("Starting radio . . .")

    playlists = get_playlists()
    if not playlists:
        mic.say("You don't have any playlists in your playlist file!")
        return

    # TODO(adjust mpdconf) Datei ~/.mpdconf anpassen: http://www.musicpd.org/doc/user/
    # kann eventuell auch in den Autostart?
    subprocess.call("mpd")

    # erste playlist laden und abspielen
    MPD.load(playlists[0])
    MPD.play()

    cmd = ""
    mic.say("Say exit to exit radio mode.")
    while cmd != "EXIT":
        cmd = mic.passivelisten().upper()
        handle_command(cmd, mic, playlists)
    MPD.stop()


def get_playlists(filename=jasperpath.data('text', 'playlists.txt')):
    """Return the playlist.

    Extracts the playlist from a text file.

    Arguments:
        filename {string} -- Filename to extract the playlist from.
    """
    pl_file = open(filename, "r")
    playlists = [line.replace('\n', '') for line in pl_file.readlines()]
    return playlists


def handle_command(self, cmd, mic, playlists):
    """Handle the spoken command.

    Arguments:
        cmd {object} -- Spoken command
        mic {object} -- Microphone object
        playlists {list} -- The playlists
    """
    index = 0
    if cmd == "PLAY":
        MPD.play()
    elif cmd == "STOP":
        MPD.stop()

    # Volume
    elif cmd == "VOLUME":
        cmd = mic.activeListen().upper()
        if cmd == "UP":
            MPD.vol_up()
        elif cmd == "DOWN":
            MPD.vol_down()

    # Next playlist
    elif cmd == "NEXT":
        MPD.stop()
        index += 1
        if index > len(playlists) - 1:
            index = 0
        MPD.load(playlists[index])
        MPD.play()

    # Previous playlist
    elif cmd == "PREVIOUS":
        MPD.stop()
        index -= 1
        if index < 0:
            index = len(playlists) - 1
        MPD.load(playlists[index])
        MPD.play()


def isValid(text):
    """Check if keyword is radio.

    Returns True if the input is related to the radio.

    Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bradio\b', text, re.IGNORECASE))


class MPD(object):

    @staticmethod
    def load(self, playlist):
        """Load the playlist."""
        subprocess.call("mpc load " + playlist, shell=True)

    @staticmethod
    def play(self):
        """Start the playlist."""
        subprocess.call("mpc play", shell=True)

    @staticmethod
    def stop(self):
        """Stop the playlist."""
        subprocess.call("mpc stop", shell=True)

    @staticmethod
    def vol_up(self):
        """Put the volume up by 10."""
        subprocess.call("mpc volume +10", shell=True)

    @staticmethod
    def vol_down(self):
        """Put the volume down by 10."""
        subprocess.call("mpc volume -10", shell=True)

    @staticmethod
    def next(self):
        """Change to the next playlist."""
        subprocess.call("mpc next", shell=True)

    @staticmethod
    def previous(self):
        """Change to the previous playlist."""
        subprocess.call("mpc previous", shell=True)
