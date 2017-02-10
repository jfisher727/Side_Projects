from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .forms import CaptureForm
from .forms import ScheduleForm
from .forms import PlayerStatsForm
from .forms import FantasyLeagueSettingsForm
from .forms import FantasyScoringSelect
from .forms import PlayerPredictionsForm

from .models import Player
from .models import Season
from .models import Weekly_Stats
from .models import Matchup
from .models import Fantasy_League_Settings

from .parsers.StatsParser import StatsParser
from .parsers.MatchupParser import MatchupParser

from .calculators.scoring_calculator import PointsCalculator
from .calculators.predictions import PlayerPredictions

import requests

# Create your views here.


def index(request):
    seasons = []
    all_seasons = Season.objects.all().order_by('season')
    for season in all_seasons:
        if season.season not in seasons:
            seasons.append(season.season)
    return render(request, 'FantasyFootball/index.html', {'seasons': seasons})


def season_matchups(request, season_number):
    season_matchups = Matchup.objects.filter(season=season_number).order_by('week')
    weekly_matchups = {}
    for matchup in season_matchups:
        week = matchup.week
        if week in weekly_matchups:
            weekly_matchups[week].append(matchup)
        else:
            weekly_matchups[week] = [matchup]
    return render(request, 'FantasyFootball/season_matchups.html', {'weekly_matchups': weekly_matchups})


def matchup_boxscore(request, matchup_id):
    current_matchup = get_object_or_404(Matchup, pk=matchup_id)
    matchup_stats = Weekly_Stats.objects.filter(matchup=matchup_id)
    home_team = []
    away_team = []
    for stats in matchup_stats:
        this_season = Season.objects.filter(id=stats.season.id).first()
        if this_season.team == current_matchup.home_team:
            home_team.append(stats)
        elif this_season.team == current_matchup.away_team:
            away_team.append(stats)

    return render(request, 'FantasyFootball/matchup_boxscore.html', {'matchup': current_matchup,
                                                                     'home_team': home_team,
                                                                     'away_team': away_team})


def get_league_settings_request(request):
    if request.method == "POST":
        form = FantasyLeagueSettingsForm(request.POST)

        if form.is_valid():
            settings_name = form.cleaned_data['name']

            if not Fantasy_League_Settings.objects.filter(name=settings_name).exists():
                settings = form.save(commit=True)

        return redirect('all_league_settings_display')
    else:
        form = FantasyLeagueSettingsForm()
    return render(request, 'FantasyFootball/league_settings_request.html', {'form': form})


def league_settings_display(request, settings_id):
    league_settings = get_object_or_404(Fantasy_League_Settings, pk=settings_id)
    return render(request, 'FantasyFootball/league_settings_display.html', {'league_settings': league_settings})


def all_league_settings_display(request):
    all_league_settings = Fantasy_League_Settings.objects.all()
    return render(request, 'FantasyFootball/all_league_settings.html', {'league_settings': all_league_settings})


def update_entries(request):
    if request.method == "POST":
        positions = {'10': 'QB', '20': 'RB', '30': 'WR', '40': 'TE', '80': 'K', '99': 'DEF'}

        form = ScheduleForm(request.POST)
        if form.is_valid():
            season = form.cleaned_data['season']
            week = form.cleaned_data['week']

            # capture the matchups, then capture the player data for the week
            if 'ALL' in week:
                for x in range(1, 18):
                    existing_players = Player.objects.all()
                    existing_seasons = Season.objects.filter(season=season)
                    existing_weekly_stats = Weekly_Stats.objects.filter(season=season, week=x)
                    existing_matchups = Matchup.objects.filter(season=season, week=x)

                    schedule_data = requests.get('http://www.nfl.com/scores/%s/REG%s' % (season, str(x)))
                    if schedule_data.status_code == 200:
                        parser = MatchupParser(schedule_data.text, existing_matchups, season, x)
                    else:
                        print("Error completing the schedule request")

                    existing_matchups = Matchup.objects.filter(season=season, week=x)
                    for key in positions.keys():
                        position_name = positions[key]
                        stats_data = requests.get('http://fftoday.com/stats/playerstats.php?Season=%s&GameWeek=%s&PosID=%s' % (season, str(x), key))
                        if stats_data.status_code == 200:
                            StatsParser(stats_data.text,
                                        existing_players,
                                        existing_seasons,
                                        existing_weekly_stats,
                                        existing_matchups,
                                        position_name,
                                        season,
                                        x)
                        else:
                            print("Error completing the stats request")
            else:
                existing_players = Player.objects.all()
                existing_seasons = Season.objects.filter(season=season)
                existing_weekly_stats = Weekly_Stats.objects.filter(season=season, week=week)
                existing_matchups = Matchup.objects.filter(season=season, week=week)

                schedule_data = requests.get('http://www.nfl.com/scores/%s/REG%s' % (season, str(week)))
                if schedule_data.status_code == 200:
                    parser = MatchupParser(schedule_data.text, existing_matchups, season, week)
                else:
                    print("Error completing the schedule request")

                existing_matchups = Matchup.objects.filter(season=season, week=week)
                for key in positions.keys():
                    position_name = positions[key]
                    stats_data = requests.get('http://fftoday.com/stats/playerstats.php?Season=%s&GameWeek=%s&PosID=%s' % (season, week, key))
                    if stats_data.status_code == 200:
                        StatsParser(stats_data.text,
                                    existing_players,
                                    existing_seasons,
                                    existing_weekly_stats,
                                    existing_matchups,
                                    position_name,
                                    season,
                                    week)
                    else:
                        print("Error completing the stats request")

        return render(request, 'FantasyFootball/update_db_response.html', {})
    else:
        form = ScheduleForm()
    return render(request, 'FantasyFootball/update_db_request.html', {'form': form})


def get_player_stats(request):
    if request.method == "POST":
        form = PlayerStatsForm(request.POST)
        applicable_players = []
        if form.is_valid():
            position = form.cleaned_data['position']
            team = form.cleaned_data['team']
            player_name = form.cleaned_data['player_name']

            applicable_players = Player.objects.all().order_by('name')

            if player_name:
                applicable_players = applicable_players.filter(name__icontains=player_name)

            if 'ANY' not in position:
                applicable_players = applicable_players.filter(position=position).order_by('name')

            if 'ANY' not in team:
                updated_players = []
                for player in applicable_players:
                    player_seasons = Season.objects.filter(player_id=player.id)
                    for season in player_seasons:
                        if season.team == team:
                            updated_players.append(player)
                            break
                applicable_players = updated_players

        return render(request, 'FantasyFootball/player_query_display.html',
                      {'applicable_players': applicable_players, 'form': form})
    else:
        form = PlayerStatsForm()

        return render(request, 'FantasyFootball/player_stats_request.html', {'form': form})


def player_details(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    seasons = Season.objects.filter(player=player_id).order_by('season')
    total_season_stats = {}
    for season in seasons:
        season_total = Weekly_Stats(season=season,
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
        all_season_stats = Weekly_Stats.objects.filter(season_id=season.id)
        for stats in all_season_stats:
            season_total = stats + season_total
        total_season_stats[str(season.season)] = season_total
    return render(request, 'FantasyFootball/player_seasons_display.html', {'player': player,
                                                                           'seasons': seasons,
                                                                           'season_stats': total_season_stats})


def season_details(request, player_id, season_id):
    form = FantasyScoringSelect()
    season = get_object_or_404(Season, pk=season_id)
    player = get_object_or_404(Player, pk=player_id)
    weekly_stats = Weekly_Stats.objects.filter(season=season.id).order_by('week')
    for week in weekly_stats:
        current_matchup = week.matchup
        # if our player is the away team
        if not current_matchup.home_team == season.team and current_matchup.away_team == season.team:
            week.opponent = current_matchup.home_team
            if current_matchup.away_score > current_matchup.home_score:
                week.result = 'W'
            elif current_matchup.away_score < current_matchup.home_score:
                week.result = 'L'
            elif current_matchup.away_score == current_matchup.home_score:
                week.result = 'T'
            else:
                print('Unable to determine result')
        # elif our player is the home team
        elif current_matchup.home_team == season.team and not current_matchup.away_team == season.team:
            week.opponent = current_matchup.away_team
            if current_matchup.away_score > current_matchup.home_score:
                week.result = 'L'
            elif current_matchup.away_score < current_matchup.home_score:
                week.result = 'W'
            elif current_matchup.away_score == current_matchup.home_score:
                week.result = 'T'
            else:
                print('Unable to determine result')
        else:
            print('Couldnt figure out who the opponent was')

        if request.method == "POST":
            form = FantasyScoringSelect(request.POST)
            if form.is_valid():
                selected = form.cleaned_data['fantasy_league_settings']
                week.fantasy_points = PointsCalculator.CalculatePoints(week, selected, player.position)
    return render(request, 'FantasyFootball/season_stats_display.html', {'player': player,
                                                                         'season': season,
                                                                         'weekly_stats': weekly_stats,
                                                                         'form': form})


def get_player_prediction(request):
    if request.method == "POST":
        form = PlayerPredictionsForm(request.POST)
        player_predictions = []

        if form.is_valid():
            position_input = form.cleaned_data['position']
            team_input = form.cleaned_data['team']
            season_input = form.cleaned_data['season']
            week_input = form.cleaned_data['week']
            selected_settings = form.cleaned_data['fantasy_league_settings']

            applicable_players = Player.objects.all().order_by('name')

            if 'ANY' not in position_input:
                applicable_players = applicable_players.filter(position=position_input).order_by('name')

            if 'ANY' not in team_input:
                updated_players = []
                for player in applicable_players:
                    player_seasons = Season.objects.filter(player_id=player.id, season=season_input)
                    for season in player_seasons:
                        if season.team == team_input:
                            updated_players.append(player)
                            break
                applicable_players = updated_players

            predictor = PlayerPredictions()

            for player in applicable_players:
                predicted_stats = predictor.prediction(player, season_input, week_input)
                predicted_stats.fantasy_points = PointsCalculator.CalculatePoints(predicted_stats,
                                                                                  selected_settings,
                                                                                  player.position)
                print(predicted_stats.fantasy_points)
                player_predictions.append(predicted_stats)

            return render(request, 'FantasyFootball/player_predictions_display.html',
                          {'form': form,
                           'player_predictions': player_predictions,
                           'applicable_players': applicable_players})
    else:
        form = PlayerPredictionsForm()
    return render(request, 'FantasyFootball/player_predictions_request.html', {'form': form})
