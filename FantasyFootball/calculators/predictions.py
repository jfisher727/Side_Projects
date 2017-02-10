
from FantasyFootball.models import Player
from FantasyFootball.models import Season
from FantasyFootball.models import Weekly_Stats
from FantasyFootball.models import Matchup


class PlayerPredictions():

    def find_weeks_playing_opponent(self, player, opponent):
        stats_against_opponent = []
        this_player_seasons = Season.objects.filter(player_id=player.id)

        for season in this_player_seasons:
            this_season_weekly_stats = Weekly_Stats.objects.filter(season=season.id)
            for weekly_stats in this_season_weekly_stats:
                this_week_matchup = Matchup.objects.filter(id=weekly_stats.matchup.id).first()
                if this_week_matchup.home_team == opponent or this_week_matchup.away_team == opponent:
                    stats_against_opponent.append(weekly_stats)

        return stats_against_opponent

    def find_weeks_playing_home_or_away(self, player, home_game):
        stats_home_or_away = []
        this_player_seasons = Season.objects.filter(player_id=player.id)

        for season in this_player_seasons:
            this_season_weekly_stats = Weekly_Stats.objects.filter(season=season.id)
            for weekly_stats in this_season_weekly_stats:
                this_week_matchup = Matchup.objects.filter(id=weekly_stats.matchup.id).first()
                if home_game and this_week_matchup.home_team == season.team:
                    stats_home_or_away.append(weekly_stats)
                elif not home_game and this_week_matchup.away_team == season.team:
                    stats_home_or_away.append(weekly_stats)

        return stats_home_or_away

    def prediction(self, player, season_number, week_number):
        matchups = Matchup.objects.filter(season=season_number, week=week_number)
        this_player_seasons = Season.objects.filter(player_id=player.id)
        current_team = Season.objects.filter(player_id=player.id, season=season_number).first().team

        opponent = ""
        home_game = False
        for matchup in matchups:
            if matchup.home_team == current_team and not matchup.away_team == current_team:
                opponent = matchup.away_team
                home_game = True
                break
            elif not matchup.home_team == current_team and matchup.away_team == current_team:
                opponent = matchup.home_team
                home_game = False
                break

        average_opponent_stats = ""
        average_division_stats = ""
        average_home_away_stats = ""
        average_season_stats = ""

        stats_against_opponent = self.find_weeks_playing_opponent(player, opponent)

        if len(stats_against_opponent) > 0:
            cumulative_stats = Weekly_Stats(season=stats_against_opponent[0].season,
                                            passing_completions=0,
                                            passing_attempts=0,
                                            passing_yards=0,
                                            passing_td=0,
                                            passing_int=0,
                                            rushing_attempts=0,
                                            rushing_yards=0,
                                            rushing_td=0,
                                            receiving_targets=0,
                                            receiving_receptions=0,
                                            receiving_yards=0,
                                            receiving_td=0,
                                            field_goal_made=0,
                                            field_goal_attempts=0,
                                            extra_point_made=0,
                                            extra_point_attempts=0,
                                            sacks=0,
                                            fumble_recovery=0,
                                            interceptions=0,
                                            defensive_td=0,
                                            points_against=0,
                                            passing_yards_against=0,
                                            rushing_yards_against=0,
                                            safety=0,
                                            kick_return_td=0
                                            )
            for game in stats_against_opponent:
                cumulative_stats += game
            average_opponent_stats = cumulative_stats.average(len(stats_against_opponent))
            divisional_stats = cumulative_stats
            divisional_games = len(stats_against_opponent)
        else:
            print("Couldn't find enough data against this opponent")
            divisional_stats = ""
            divisional_games = 0

        for key in self.nfl_divisions.keys():
            if opponent in self.nfl_divisions[key]:
                divisional_opponents = self.nfl_divisions[key]
                for division in divisional_opponents:
                    if not division == opponent:
                        opponent_stats = self.find_weeks_playing_opponent(player, division)
                        if divisional_stats == "" and len(opponent_stats) > 0:
                            divisional_stats = Weekly_Stats(season=opponent_stats[0].season,
                                                            passing_completions=0,
                                                            passing_attempts=0,
                                                            passing_yards=0,
                                                            passing_td=0,
                                                            passing_int=0,
                                                            rushing_attempts=0,
                                                            rushing_yards=0,
                                                            rushing_td=0,
                                                            receiving_targets=0,
                                                            receiving_receptions=0,
                                                            receiving_yards=0,
                                                            receiving_td=0,
                                                            field_goal_made=0,
                                                            field_goal_attempts=0,
                                                            extra_point_made=0,
                                                            extra_point_attempts=0,
                                                            sacks=0,
                                                            fumble_recovery=0,
                                                            interceptions=0,
                                                            defensive_td=0,
                                                            points_against=0,
                                                            passing_yards_against=0,
                                                            rushing_yards_against=0,
                                                            safety=0,
                                                            kick_return_td=0
                                                            )
                        for stats in opponent_stats:
                            divisional_stats += stats
                            divisional_games += 1
                average_division_stats = divisional_stats.average(divisional_games)
                break

        home_or_away_stats = self.find_weeks_playing_home_or_away(player, home_game)
        if len(home_or_away_stats) > 0:
            cumulative_home_away_stats = Weekly_Stats(season=home_or_away_stats[0].season,
                                                      passing_completions=0,
                                                      passing_attempts=0,
                                                      passing_yards=0,
                                                      passing_td=0,
                                                      passing_int=0,
                                                      rushing_attempts=0,
                                                      rushing_yards=0,
                                                      rushing_td=0,
                                                      receiving_targets=0,
                                                      receiving_receptions=0,
                                                      receiving_yards=0,
                                                      receiving_td=0,
                                                      field_goal_made=0,
                                                      field_goal_attempts=0,
                                                      extra_point_made=0,
                                                      extra_point_attempts=0,
                                                      sacks=0,
                                                      fumble_recovery=0,
                                                      interceptions=0,
                                                      defensive_td=0,
                                                      points_against=0,
                                                      passing_yards_against=0,
                                                      rushing_yards_against=0,
                                                      safety=0,
                                                      kick_return_td=0
                                                      )
            for game in home_or_away_stats:
                cumulative_home_away_stats += game

            average_home_away_stats = cumulative_home_away_stats.average(len(home_or_away_stats))
        else:
            print("Couldn't find enough data for home or away games.")

        selected_season = Season.objects.filter(season=season_number, player_id=player.id).first()
        selected_season_stats = Weekly_Stats.objects.filter(season_id=selected_season.id)
        if len(selected_season_stats) > 0:
            cumulative_season_stats = Weekly_Stats(season=selected_season,
                                                   passing_completions=0,
                                                   passing_attempts=0,
                                                   passing_yards=0,
                                                   passing_td=0,
                                                   passing_int=0,
                                                   rushing_attempts=0,
                                                   rushing_yards=0,
                                                   rushing_td=0,
                                                   receiving_targets=0,
                                                   receiving_receptions=0,
                                                   receiving_yards=0,
                                                   receiving_td=0,
                                                   field_goal_made=0,
                                                   field_goal_attempts=0,
                                                   extra_point_made=0,
                                                   extra_point_attempts=0,
                                                   sacks=0,
                                                   fumble_recovery=0,
                                                   interceptions=0,
                                                   defensive_td=0,
                                                   points_against=0,
                                                   passing_yards_against=0,
                                                   rushing_yards_against=0,
                                                   safety=0,
                                                   kick_return_td=0
                                                   )
            for stats in selected_season_stats:
                cumulative_season_stats += stats

            average_season_stats = cumulative_season_stats.average(len(selected_season_stats))

        calculated_stats = 0
        predicted_stats = ""
        if not average_season_stats == "":
            predicted_stats = average_season_stats
            calculated_stats += 1
        if not average_division_stats == "":
            if predicted_stats == "":
                predicted_stats = average_division_stats
            else:
                predicted_stats += average_division_stats
            calculated_stats += 1
        if not average_home_away_stats == "":
            if predicted_stats == "":
                predicted_stats = average_home_away_stats
            else:
                predicted_stats += average_home_away_stats
            calculated_stats += 1
        if not average_opponent_stats == "":
            if predicted_stats == "":
                predicted_stats = average_opponent_stats
            else:
                predicted_stats += average_opponent_stats
            calculated_stats += 1

        return predicted_stats.average(calculated_stats)

    def __init__(self):
        self.nfl_divisions = {'AFC East': ['Dolphins', 'Patriots', 'Jets', 'Bills'],
                              'AFC South': ['Jaguars', 'Colts', 'Titans', 'Texans'],
                              'AFC North': ['Steelers', 'Ravens', 'Bengals', 'Browns'],
                              'AFC West': ['Broncos', 'Chiefs', 'Chargers', 'Raiders'],
                              'NFC East': ['Cowboys', 'Giants', 'Eagles', 'Redskins'],
                              'NFC South': ['Saints', 'Panthers', 'Falcons', 'Buccaneers'],
                              'NFC North': ['Packers', 'Vikings', 'Bears', 'Lions'],
                              'NFC West': ['Seahawks', 'Rams', 'Cardinals', '49ers'],
                              }
