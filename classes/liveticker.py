# -*- coding: utf-8-*-
import datetime
import json
import requests

class Liveticker:

    # API Endpoint of the OpenLigaDB Database for football match data
    API = "http://www.openligadb.de/api/"

    
    def __init__(self, team, league):
    """
        Initialization of the Liveticker module.
        Initialized properties:
            ::team
            ::league
            ::season
            ::matchday
        """
    self.team = team
    self.league = league
    self.season = get_current_season()
    self.matchday = get_current_matchday()
    

    def get_current_season(self):
        """ 
            Get the current season of the league.
            Seasons change in July of each year.
        """
        if date.today().month < 7:
            return date.today().year - 1
        return date.today().year
        
    def get_current_matchday(self):
        """
            Returns: the current matchday of the season
        """
        return json.loads(requests.get(API + "getcurrentgroup/" + self.league).text)["GroupOrderID"]

    def get_last_change_date(self):
        """
            Returns: the last change date of the current matchday
        """
        return json.loads(requests.get((API + "getlastchangedate/" + self.league + "/" + str(self.season) + "/" + str(self.matchday))).text)

    def get_match_data(self):
        """
            Returns: a dict object with the current match data for the supported team
        """
        response = json.loads(requests.get(API + "getmatchdata/" + self.league + "/" + str(self.season) + "/" + str(self.matchday)).text)
        for spiel in response:
            if get_team(spiel, 1) == self.team or get_team(spiel, 2) == self.team:
                return spiel
        return {}
    
    @staticmethod
    def get_team(match_data, teamNr):
        """
            Returns: name of the team with the given teamNr
        """
        return match_data["Team" + str(teamNr)]["TeamName"]

    @staticmethod
    def get_goals(match_data, teamNr):
        """
            Returns: amount of goals of the team with the given teamNr
        """
        return match_data["ScoreTeam" + str(teamNr)]
        
    @staticmethod
    def get_last_goal(match_data):
        """
            Returns: the dict of the last scored goal of the given match data
        """
        last_goal = ["GoalID" : "0"]
        if match_data["Goals"]:
            for goal in match_data["Goals"]:
                if goal["GoalID"] > last_goal["GoalID"]:
                    last_goal = goal
        return last_goal
        
    @staticmethod
    def format_goal(goal):
        """ Format a dict object with the form:
                Team1
                    TeamName
                Team2
                    TeamName
                ScoreTeam1
                ScoreTeam2
                MatchMinute
                GoalGetterName
            
            Returns: the formatted string
        """
        home_team = match_data["Team1"]["TeamName"]
        away_team = match_data["Team2"]["TeamName"]
        home_score = goal["ScoreTeam1"]
        away_score = goal["ScoreTeam2"]
        match_minute = goal["MatchMinute"]
        goal_getter = goal["GoalGetterName"]
        return ("Goal by " + goal_getter + " in the " + str(match_minute) + ". Minute! New score: "
                + home_team + " " + str(home_score) + " " + away_team + " " + str(away_score))
    