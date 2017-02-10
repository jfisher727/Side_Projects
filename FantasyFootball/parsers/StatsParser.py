from html.parser import HTMLParser
import requests

from .FFPlayer import FFPlayer

from django.db.models import Q

from FantasyFootball.models import Player
from FantasyFootball.models import Season
from FantasyFootball.models import Weekly_Stats
from FantasyFootball.models import Matchup


class StatsParser(HTMLParser):

    def handle_starttag(self, tag, attributes):
        self.current_tag = tag
        if self.current_tag == "a":
            for attribute in attributes:
                if "/stats/player" in attribute[1]:
                    self.player_found = True
                    self.current_player = FFPlayer()
                    self.current_player.set_season(self.season)
                    self.current_player.set_week(self.week)
                    self.current_player.set_position(self.position)
                    self.current_link = attribute[1]

    def handle_endtag(self, tag):
        self.current_tag = ""
        if tag == "tr" and self.player_found:
            self.player_found = False
            if not self.current_player == "":
                if ("players" not in self.current_player.name and
                    "page" not in self.current_player.name.lower() and
                    "page" not in self.current_player.team.lower() and
                    not self.current_player.name == "" and
                    not self.failed_to_convert):
                        # transform the data from the FFPlayer object to the Database entries
                        this_player = Player(name=self.current_player.name, position=self.current_player.position)

                        # checks to see if this player is new or there is one with the same name and position
                        if self.existing_players.filter(name=this_player.name, position=this_player.position).exists():
                            this_player = self.existing_players.filter(name=this_player.name,
                                                                       position=this_player.position).first()
                        else:
                            this_player.save()

                        this_season = Season(team=self.team_names[self.current_player.team],
                                                                  season=self.current_player.season,
                                                                  player=this_player)

                        # checks if there is a season which already exists with this team, season number, and reference to the same player
                        if self.existing_seasons.filter(team=this_season.team,
                                                        season=this_season.season,
                                                        player=this_season.player).exists():
                            this_season = self.existing_seasons.filter(team=this_season.team,
                                                                       season=this_season.season,
                                                                       player=this_season.player).first()
                        else:
                            this_season.save()

                        # finds the matchup for this week in the season where these two teams were playing
                        weekly_matchups = self.existing_matchups.filter(season=self.season, week=self.week)
                        this_matchup = ""
                        if weekly_matchups.filter(Q(home_team=this_season.team) | Q(away_team=this_season.team)).exists():
                            this_matchup = weekly_matchups.filter(Q(home_team=this_season.team) | Q(away_team=this_season.team)).first()
                        else:
                            print("Error determining the matchup")

                        this_weeks_stats = Weekly_Stats(season=this_season,
                                                        matchup=this_matchup,
                                                        week=self.week,
                                                        passing_completions=self.current_player.passing_completions,
                                                        passing_attempts=self.current_player.passing_attempts,
                                                        passing_yards=self.current_player.passing_yards,
                                                        passing_td=self.current_player.passing_td,
                                                        passing_int=self.current_player.passing_int,
                                                        rushing_attempts=self.current_player.rushing_attempts,
                                                        rushing_yards=self.current_player.rushing_yards,
                                                        rushing_td=self.current_player.rushing_td,
                                                        receiving_targets=self.current_player.receiving_targets,
                                                        receiving_receptions=self.current_player.receiving_receptions,
                                                        receiving_yards=self.current_player.receiving_yards,
                                                        receiving_td=self.current_player.receiving_td,
                                                        field_goal_made=self.current_player.field_goal_made,
                                                        field_goal_attempts=self.current_player.field_goal_attempts,
                                                        extra_point_made=self.current_player.extra_point_made,
                                                        extra_point_attempts=self.current_player.extra_point_attempts,
                                                        sacks=self.current_player.sacks,
                                                        fumble_recovery=self.current_player.fumble_recovery,
                                                        interceptions=self.current_player.interceptions,
                                                        defensive_td=self.current_player.defensive_td,
                                                        points_against=self.current_player.points_against,
                                                        passing_yards_against=self.current_player.passing_yards_against,
                                                        rushing_yards_against=self.current_player.rushing_yards_against,
                                                        safety=self.current_player.safety,
                                                        kick_return_td=self.current_player.kick_return_td)

                        # checks to make sure theres no weekly stats entries with the same stats
                        if not self.existing_weekly_stats.filter(season=this_season.id,
                                                                 matchup=this_matchup.id,
                                                                 week=this_weeks_stats.week,
                                                                 passing_completions=this_weeks_stats.passing_completions,
                                                                 passing_attempts=this_weeks_stats.passing_attempts,
                                                                 passing_yards=this_weeks_stats.passing_yards,
                                                                 passing_td=this_weeks_stats.passing_td,
                                                                 passing_int=this_weeks_stats.passing_int,
                                                                 rushing_attempts=this_weeks_stats.rushing_attempts,
                                                                 rushing_yards=this_weeks_stats.rushing_yards,
                                                                 rushing_td=this_weeks_stats.rushing_td,
                                                                 receiving_targets=this_weeks_stats.receiving_targets,
                                                                 receiving_receptions=this_weeks_stats.receiving_receptions,
                                                                 receiving_yards=this_weeks_stats.receiving_yards,
                                                                 receiving_td=this_weeks_stats.receiving_td,
                                                                 field_goal_made=this_weeks_stats.field_goal_made,
                                                                 field_goal_attempts=this_weeks_stats.field_goal_attempts,
                                                                 sacks=this_weeks_stats.sacks,
                                                                 fumble_recovery=this_weeks_stats.fumble_recovery,
                                                                 interceptions=this_weeks_stats.interceptions,
                                                                 defensive_td=this_weeks_stats.defensive_td,
                                                                 points_against=this_weeks_stats.points_against,
                                                                 passing_yards_against=this_weeks_stats.passing_yards_against,
                                                                 rushing_yards_against=this_weeks_stats.rushing_yards_against,
                                                                 safety=this_weeks_stats.safety,
                                                                 kick_return_td=this_weeks_stats.kick_return_td).exists():
                            this_weeks_stats.save()
                # self.all_players_found.append(self.current_player)
                self.current_player = ""
                self.failed_to_convert = False
                self.data_index = 0

    def handle_data(self, data):
        if self.player_found and (self.current_tag == "td" or self.current_tag == "a"):

            if self.position == "DEF":
                if self.data_index == 0:  # name
                    if " " in data:
                        abreviated_name = self.team_names[data[data.rfind(' ') + 1:]]
                        self.current_player.set_name(data)
                        self.current_player.set_team(abreviated_name)
                elif self.data_index == 1:  # games
                    pass
                elif self.data_index == 2:  # sacks
                    self.failed_to_convert = self.current_player.set_sacks(data)
                elif self.data_index == 3:
                    self.failed_to_convert = self.current_player.set_fumble_recoveries(data)
                elif self.data_index == 4:
                    self.failed_to_convert = self.current_player.set_interceptions(data)
                elif self.data_index == 5:
                    self.failed_to_convert = self.current_player.set_defensive_td(data)
                elif self.data_index == 6:
                    self.failed_to_convert = self.current_player.set_points_against(data)
                elif self.data_index == 7:
                    self.failed_to_convert = self.current_player.set_passing_yards_against(data)
                elif self.data_index == 8:
                    self.failed_to_convert = self.current_player.set_rushing_yards_against(data)
                elif self.data_index == 9:
                    self.failed_to_convert = self.current_player.set_safety(data)
                elif self.data_index == 10:
                    self.failed_to_convert = self.current_player.set_kick_return_td(data)
            else:
                if self.data_index == 0:  # name
                    self.current_player.set_name(data)
                elif self.data_index == 1:  # team
                    self.current_player.set_team(data)
                elif self.data_index == 2:  # games
                    pass

                if self.position == "QB":
                    if self.data_index == 3:  # passing comp
                        self.current_player.set_passing_completions(data)
                    elif self.data_index == 4:  # passing att
                        self.current_player.set_passing_attempts(data)
                    elif self.data_index == 5:  # passing yards
                        self.current_player.set_passing_yards(data)
                    elif self.data_index == 6:  # passing td
                        self.current_player.set_passing_td(data)
                    elif self.data_index == 7:  # passing int
                        self.current_player.set_passing_int(data)
                    elif self.data_index == 8:  # rushing attempt
                        self.current_player.set_rushing_attempts(data)
                    elif self.data_index == 9:  # rushing yards
                        self.current_player.set_rushing_yards(data)
                    elif self.data_index == 10:  # rushing td
                        self.current_player.set_rushing_td(data)
                    else:
                        pass
                elif self.position == "RB":
                    if self.data_index == 3:
                        self.current_player.set_rushing_attempts(data)
                    elif self.data_index == 4:
                        self.current_player.set_rushing_yards(data)
                    elif self.data_index == 5:
                        self.current_player.set_rushing_td(data)
                    elif self.data_index == 6:
                        self.current_player.set_receiving_targets(data)
                    elif self.data_index == 7:
                        self.current_player.set_receiving_receptions(data)
                    elif self.data_index == 8:
                        self.current_player.set_receiving_yards(data)
                    elif self.data_index == 9:
                        self.current_player.set_receiving_td(data)
                    else:
                        pass
                elif self.position == "WR":
                    if self.data_index == 3:
                        self.current_player.set_receiving_targets(data)
                    elif self.data_index == 4:
                        self.current_player.set_receiving_receptions(data)
                    elif self.data_index == 5:
                        self.current_player.set_receiving_yards(data)
                    elif self.data_index == 6:
                        self.current_player.set_receiving_td(data)
                    elif self.data_index == 7:
                        self.current_player.set_rushing_attempts(data)
                    elif self.data_index == 8:
                        self.current_player.set_rushing_yards(data)
                    elif self.data_index == 9:
                        self.current_player.set_rushing_td(data)
                    else:
                        pass
                elif self.position == "TE":
                    if self.data_index == 3:
                        self.current_player.set_receiving_targets(data)
                    elif self.data_index == 4:
                        self.current_player.set_receiving_receptions(data)
                    elif self.data_index == 5:
                        self.current_player.set_receiving_yards(data)
                    elif self.data_index == 6:
                        self.current_player.set_receiving_td(data)
                    else:
                        pass
                elif self.position == "K":
                    if self.data_index == 3:
                        self.current_player.set_field_goal_made(data)
                    elif self.data_index == 4:
                        self.current_player.set_field_goal_attempt(data)
                    elif self.data_index == 5:
                        pass
                    elif self.data_index == 6:
                        self.current_player.set_extra_point_made(data)
                    elif self.data_index == 7:
                        self.current_player.set_extra_point_attempt(data)
                    else:
                        pass
                    pass
            self.data_index += 1

        if self.current_tag == "a" and "next page" in data.lower():
            player_data = requests.get('http://fftoday.com/%s' % self.current_link)
            if player_data.status_code == 200:
                existing_players = Player.objects.all()
                existing_seasons = Season.objects.filter(season=self.season)
                existing_weekly_stats = Weekly_Stats.objects.filter(season=self.season, week=self.week)
                existing_matchups = Matchup.objects.filter(season=self.season, week=self.week)
                StatsParser(player_data.text,
                            existing_players,
                            existing_seasons,
                            existing_weekly_stats,
                            existing_matchups,
                            self.position,
                            self.season,
                            self.week)
            else:
                print("Error completing the stats request")

    def __init__(self, data, existing_players, existing_seasons, existing_weekly_stats, existing_matchups, position,  season, week):
        HTMLParser.__init__(self)
        self.team_names = {'Cardinals': 'Cardinals', 'ARI': 'Cardinals',
                           'Falcons': 'Falcons', 'ATL': 'Falcons',
                           'Ravens': 'Ravens', 'BAL': 'Ravens',
                           'Bills': 'Bills', 'BUF': 'Bills',
                           'Panthers': 'Panthers', 'CAR': 'Panthers',
                           'Bears': 'Bears', 'CHI': 'Bears',
                           'Bengals': 'Bengals', 'CIN': 'Bengals',
                           'Browns': 'Browns', 'CLE': 'Browns',
                           'Cowboys': 'Cowboys', 'DAL': 'Cowboys',
                           'Broncos': 'Broncos', 'DEN': 'Broncos',
                           'Lions': 'Lions', 'DET': 'Lions',
                           'Packers': 'Packers', 'GB': 'Packers',
                           'Texans': 'Texans', 'HOU': 'Texans',
                           'Colts': 'Colts', 'IND': 'Colts',
                           'Jaguars': 'Jaguars', 'JAC': 'Jaguars', 'JAX': 'Jaguars',
                           'Chiefs': 'Chiefs', 'KC': 'Chiefs',
                           'Dolphins': 'Dolphins', 'MIA': 'Dolphins',
                           'Vikings': 'Vikings', 'MIN': 'Vikings',
                           'Patriots': 'Patriots', 'NE': 'Patriots',
                           'Saints': 'Saints', 'NO': 'Saints',
                           'Giants': 'Giants', 'NYG': 'Giants',
                           'Jets': 'Jets', 'NYJ': 'Jets',
                           'Raiders': 'Raiders', 'OAK': 'Raiders',
                           'Eagles': 'Eagles', 'PHI': 'Eagles',
                           'Steelers': 'Steelers', 'PIT': 'Steelers',
                           'Chargers': 'Chargers', 'SD': 'Chargers', 'LAC': 'Chargers',
                           '49ers': '49ers', 'SF': '49ers',
                           'Seahawks': 'Seahawks', 'SEA': 'Seahawks',
                           'Rams': 'Rams', 'STL': 'Rams', 'LAR': 'Rams',
                           'Buccaneers': 'Buccaneers', 'TB': 'Buccaneers',
                           'Titans': 'Titans', 'TEN': 'Titans',
                           'Redskins': 'Redskins', 'WAS': 'Redskins',
                           }

        self.player_found = False
        self.failed_to_convert = False
        self.all_players_found = []
        self.current_player = ""
        self.current_tag = ""
        self.current_link = ""
        self.data_index = 0
        self.existing_players = existing_players
        self.existing_seasons = existing_seasons
        self.existing_weekly_stats = existing_weekly_stats
        self.existing_matchups = existing_matchups
        self.position = position
        self.season = season
        self.week = week
        self.feed(data)
