from html.parser import HTMLParser

import datetime

import requests

from FantasyFootball.models import Matchup


class MatchupParser(HTMLParser):

    def handle_starttag(self, tag, attributes):
        current_tag = tag
        class_attributes = ""
        if len(attributes) >= 1:
            for att in attributes:
                if 'class' in att:
                    current_tag = current_tag + " " + att[1]
                    class_attributes = att
        self.tag_tree.append(current_tag)
        if len(class_attributes) >= 1:
            if tag == 'div' and class_attributes[1] == 'scorebox-wrapper':
                self.matchup_found = True
                self.current_matchup = Matchup()
                self.current_matchup.season = self.season
                self.current_matchup.week = self.week
            elif (self.matchup_found and
                  not self.home_team_found and
                  tag == 'div' and
                  class_attributes[1] == 'away-team'):
                    self.away_team_found = True
            elif (self.matchup_found and
                  not self.away_team_found and
                  tag == 'div' and
                  class_attributes[1] == 'home-team'):
                    self.home_team_found = True
            elif self.matchup_found and tag == 'p' and class_attributes[1] == 'team-name':
                self.team_name_found = True
            elif self.matchup_found and tag == 'p' and class_attributes[1] == 'total-score':
                self.team_score_found = True

    def handle_endtag(self, tag):
        if len(self.tag_tree) >= 1:
            removed_tag = self.tag_tree.pop()
            if 'away-team' in removed_tag:
                self.away_team_found = False
            elif 'home-team' in removed_tag:
                self.home_team_found = False
            elif 'date' in removed_tag:
                self.air_date_found = False
            elif 'scorebox-wrapper' in removed_tag:
                self.matchup_found = False
                # check to make sure all the fields are set, then we can save the object
                if (self.current_matchup.home_team is not None and
                    self.current_matchup.away_team is not None and
                    self.current_matchup.home_score is not None and
                    self.current_matchup.away_score is not None):
                        if not self.existing_matchups.filter(season=self.season,
                                                             week=self.week,
                                                             home_team=self.current_matchup.home_team,
                                                             away_team=self.current_matchup.away_team).exists():
                            self.current_matchup.save()
                        else:
                            this_saved_matchup = self.existing_matchups.filter(season=self.season,
                                                                               week=self.week,
                                                                               home_team=self.current_matchup.home_team,
                                                                               away_team=self.current_matchup.away_team).first()
                            if this_saved_matchup.home_score is None or this_saved_matchup.away_score is None:
                                this_saved_matchup.home_score = self.current_matchup.home_score
                                this_saved_matchup.away_score = self.current_matchup.away_score
                                this_saved_matchup.save()
                        self.current_matchup = ""

    def handle_data(self, data):
        if self.matchup_found:
            if self.away_team_found:
                if 'team-name' in self.tag_tree[-2]:
                    self.current_matchup.away_team = self.team_names[data]
                elif 'total-score' in self.tag_tree[-1]:
                    self.current_matchup.away_score = data
            elif self.home_team_found:
                if 'team-name' in self.tag_tree[-2]:
                    self.current_matchup.home_team = self.team_names[data]
                elif 'total-score' in self.tag_tree[-1]:
                    self.current_matchup.home_score = data

    def __init__(self, data, existing_matchups, season, week):
        self.team_names = {'Cardinals': 'Cardinals', 'Falcons': 'Falcons',
                           'Ravens': 'Ravens', 'Bills': 'Bills',
                           'Panthers': 'Panthers', 'Bears': 'Bears',
                           'Bengals': 'Bengals', 'Browns': 'Browns',
                           'Cowboys': 'Cowboys', 'Broncos': 'Broncos',
                           'Lions': 'Lions', 'Packers': 'Packers',
                           'Texans': 'Texans', 'Colts': 'Colts',
                           'Jaguars': 'Jaguars', 'Chiefs': 'Chiefs',
                           'Dolphins': 'Dolphins', 'Vikings': 'Vikings',
                           'Patriots': 'Patriots', 'Saints': 'Saints',
                           'Giants': 'Giants', 'Jets': 'Jets',
                           'Raiders': 'Raiders', 'Eagles': 'Eagles',
                           'Steelers': 'Steelers', 'Chargers': 'Chargers',
                           '49ers': '49ers', 'Seahawks': 'Seahawks',
                           'Rams': 'Rams', 'Buccaneers': 'Buccaneers',
                           'Titans': 'Titans', 'Redskins': 'Redskins'
                           }

        HTMLParser.__init__(self)
        self.tag_tree = []
        self.season = season
        self.week = week

        self.existing_matchups = existing_matchups

        self.matchup_found = False
        self.away_team_found = False
        self.home_team_found = False
        self.team_name_found = False
        self.team_score_found = False
        self.air_date_found = False
        self.current_matchup = Matchup()

        self.feed(data)
