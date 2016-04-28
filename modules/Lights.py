# -*- coding: utf-8-*-

"""
Switch lights on or off.

Run the following before using this module:
    (sudo apt-get install git-core)
    git clone git://git.drogon.net/wiringPi
    cd wiringPi
    ./build
    cd
    git clone git://github.com/xkonni/raspberry-remote.git
    cd raspberry-remote
    make send
"""

import re
import subprocess

WORDS = ["LIGHT"]

systemcode = 10101

socket = 1


def isValid(text):
    """Validate the call of this module."""
    return bool(re.search(r'\blight\b', text, re.IGNORECASE))


def handle(text, mic, profile):
    """Handle the answer."""

    mic.say("Should I turn the light on or off?")

    answer = mic.activeListen()

    if 'on' in answer.lower():
        mic.say("Turning the light on")
        subprocess.call('sudo ./send ' + systemcode + ' ' +
                        socket + ' ' + 1)

    elif 'off' in text.lower():
        mic.say("Turning the light off")
        subprocess.call('sudo ./send ' + systemcode + ' ' +
                        socket + ' ' + 0)

    else:
        mic.say("Could not understand you, sorry")