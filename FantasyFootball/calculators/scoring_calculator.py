
from FantasyFootball.models import Weekly_Stats
from FantasyFootball.models import Fantasy_League_Settings


class PointsCalculator():

    def CalculatePoints(stats, scoring, position):
        passing_yards = float((stats.passing_yards / 25) * scoring.passing_points_py25)
        passing_td = (stats.passing_td * scoring.passing_td)
        passing_int = (stats.passing_int * scoring.passing_interception)

        rushing_yards = float(stats.rushing_yards * scoring.rushing_yards)
        rushing_td = (stats.rushing_td * scoring.rushing_td)

        receiving_receptions = (stats.receiving_receptions * scoring.receiving_reception)
        receiving_yards = (stats.receiving_yards * scoring.receiving_yards)
        receiving_td = (stats.receiving_td * scoring.receiving_td)

        field_goal_made = (stats.field_goal_made * scoring.field_goal_made)
        field_goal_missed = (stats.field_goal_attempts - stats.field_goal_made) * scoring.field_goal_missed
        extra_point_made = stats.extra_point_made * scoring.extra_point_made
        extra_point_missed = (stats.extra_point_attempts - stats.extra_point_made) * scoring.extra_point_missed

        sacks = stats.sacks * scoring.sacks
        fumble_recovery = stats.fumble_recovery * scoring.fumble_recovery
        interceptions = stats.interceptions * scoring.interception
        defensive_td = stats.defensive_td * scoring.defensive_td
        safety = stats.safety * scoring.safety
        kick_return_td = stats.kick_return_td * scoring.kick_return_td
        points_against = 0
        if stats.points_against == 0:
            points_against = scoring.no_points_allowed
        elif stats.points_against >= 1 and stats.points_against <= 6:
            points_against = scoring.one_six_points_allowed
        elif stats.points_against >= 7 and stats.points_against <= 13:
            points_against = scoring.seven_thirteen_points_allowed
        elif stats.points_against >= 14 and stats.points_against <= 17:
            points_against = scoring.fourteen_seventeen_points_allowed
        elif stats.points_against >= 18 and stats.points_against <= 27:
            points_against = 0
        elif stats.points_against >= 28 and stats.points_against <= 34:
            points_against = scoring.twentyeight_thirtyfour_points_allowed
        elif stats.points_against >= 35 and stats.points_against <= 45:
            points_against = scoring.thirtyfive_fourtyfive_points_allowed
        else:
            points_against = scoring.fourtysix_plus_points_allowed
        yards_against = 0
        if (stats.passing_yards_against + stats.rushing_yards_against) < 100:
            yards_against = scoring.under_hundred_total_yards_allowed
        elif ((stats.passing_yards_against + stats.rushing_yards_against) > 100 and
              (stats.passing_yards_against + stats.rushing_yards_against) < 200):
                yards_against = scoring.onehundred_twohundred_total_yards_allowed
        elif ((stats.passing_yards_against + stats.rushing_yards_against) > 200 and
              (stats.passing_yards_against + stats.rushing_yards_against) < 300):
                yards_against = scoring.twohundred_threehundred_total_yards_allowed
        elif ((stats.passing_yards_against + stats.rushing_yards_against) > 300 and
              (stats.passing_yards_against + stats.rushing_yards_against) < 350):
                yards_against = 0
        elif ((stats.passing_yards_against + stats.rushing_yards_against) > 350 and
              (stats.passing_yards_against + stats.rushing_yards_against) < 400):
                yards_against = scoring.threefifty_fourhundred_total_yards_allowed
        elif ((stats.passing_yards_against + stats.rushing_yards_against) > 400 and
              (stats.passing_yards_against + stats.rushing_yards_against) < 450):
                yards_against = scoring.fourhundred_fourfifty_total_yards_allowed
        elif ((stats.passing_yards_against + stats.rushing_yards_against) > 450 and
              (stats.passing_yards_against + stats.rushing_yards_against) < 500):
                yards_against = scoring.fourfifty_fivehundred_total_yards_allowed
        elif ((stats.passing_yards_against + stats.rushing_yards_against) > 500 and
              (stats.passing_yards_against + stats.rushing_yards_against) < 550):
                yards_against = scoring.fivehundred_fivefifty_total_yards_allowed
        else:
            yards_against = scoring.fivefifty_plus_total_yards_allowed
        if 'DEF' not in position:
            points_against = 0
            yards_against = 0
        total = "{0:.2f}".format(float(passing_yards) +
                                 float(passing_td) +
                                 float(passing_int) +
                                 float(rushing_yards) +
                                 float(rushing_td) +
                                 float(receiving_receptions) +
                                 float(receiving_yards) +
                                 float(receiving_td) +
                                 float(field_goal_made) +
                                 float(field_goal_missed) +
                                 float(extra_point_made) +
                                 float(extra_point_missed) +
                                 float(sacks) +
                                 float(fumble_recovery) +
                                 float(interceptions) +
                                 float(defensive_td) +
                                 float(safety) +
                                 float(kick_return_td) +
                                 float(points_against) +
                                 float(yards_against))
        print(total)
        print()
        return total
