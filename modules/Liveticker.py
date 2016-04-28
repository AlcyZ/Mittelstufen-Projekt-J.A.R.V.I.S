# -*- coding: utf-8-*-
import json
import requests

from classes.liveticker import Liveticker
from datetime import date

# expected words to start the module
WORDS = ["LIVETICKER"]

def handle(text, mic, profile):
    """
        Returns: the current score of the game of the supported team from the profile
    """
    if "Liveticker" in profile:
        if "team" in profile["Liveticker"] and "league" in profile["Liveticker"]:
            #retrieve the supported team
            team = profile["Liveticker"]["team"]
            #retrieve the league of the supported team
            league = profile["Liveticker"]["league"]
            
            lt = Liveticker(team, league)
            
            match_data = lt.get_match_data()
            
            if match_data:
                home_team = Liveticker.get_team(match_data, 1)
                away_team = Liveticker.get_team(match_data, 2)
                home_score = Liveticker.get_goals(match_data, 1)
                away_score = Liveticker.get_goals(match_data, 2)
                if match_data["MatchIsFinished"]:
                    output = "Match finished! %s against %s ... %s to %s." % (home_team, away_team, home_score, away_score)
                else:
                    output = "Goal! New score in the game %s against %s ... %s to %s." % (home_team, away_team, home_score, away_score)
                mic.say(output)
            else:
                mic.say("Error while reading your profile. Make sure you have set your supported team and it's league set correctly.")
        else:
            mic.say("Error. You have to specify a supported team and it's league in your profile.")
    else:
        mic.say("Error. To use the liveticker functionality, specify a supported team and it's league in your profile.")
        
def isValid(text):
    """ 
        Returns: true if the input is "liveticker"
    """
    return bool(re.search(r'\bliveticker\b', text, re.IGNORECASE))