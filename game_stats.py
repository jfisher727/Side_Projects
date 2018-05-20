from django.db import models
from django.db.models.functions import Cast

from .season import Season
from .game_result import GameResult
from .team_details import NflTeam


class GameStats(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, editable=False)
    game_result = models.ForeignKey(GameResult, on_delete=models.CASCADE, editable=False)
    team = models.ForeignKey(NflTeam, on_delete=models.CASCADE)
    # team = models.CharField(max_length=50)
    week = models.IntegerField()
    fantasy_points = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    passing_completions = models.PositiveSmallIntegerField(default=0)
    passing_attempts = models.PositiveSmallIntegerField(default=0)
    passing_yards = models.PositiveSmallIntegerField(default=0)
    passing_td = models.PositiveSmallIntegerField(default=0)
    passing_int = models.PositiveSmallIntegerField(default=0)

    rushing_attempts = models.PositiveSmallIntegerField(default=0)
    rushing_yards = models.PositiveSmallIntegerField(default=0)
    rushing_td = models.PositiveSmallIntegerField(default=0)

    receiving_targets = models.PositiveSmallIntegerField(default=0)
    receiving_receptions = models.PositiveSmallIntegerField(default=0)
    receiving_yards = models.PositiveSmallIntegerField(default=0)
    receiving_td = models.PositiveSmallIntegerField(default=0)

    field_goal_made = models.PositiveSmallIntegerField(default=0)
    field_goal_attempts = models.PositiveSmallIntegerField(default=0)
    extra_point_made = models.PositiveSmallIntegerField(default=0)
    extra_point_attempts = models.PositiveSmallIntegerField(default=0)

    sacks = models.PositiveSmallIntegerField(default=0)
    fumble_recovery = models.PositiveSmallIntegerField(default=0)
    interceptions = models.PositiveSmallIntegerField(default=0)
    defensive_td = models.PositiveSmallIntegerField(default=0)
    points_against = models.PositiveSmallIntegerField(default=0)
    passing_yards_against = models.PositiveSmallIntegerField(default=0)
    rushing_yards_against = models.PositiveSmallIntegerField(default=0)
    safety = models.PositiveSmallIntegerField(default=0)
    kick_return_td = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        if self.season.player.position == 'DEF':
            return ', '.join([str(self.season),
                              'Week: %s' % str(self.week),
                              'Points Against: %s' % self.points_against,
                              'Passing Yards Against: %s' % self.passing_yards_against,
                              'Rushing Yards Against: %s' % self.rushing_yards_against,
                              'Sacks: %s' % self.sacks,
                              'Fumble Recovery: %s' % self.fumble_recovery,
                              'Interceptions: %s' % self.interceptions,
                              'Safety: %s' % self.safety,
                              'Defensive TD: %s' % self.defensive_td,
                              'Kick Return TD: %s' % self.kick_return_td])
        return ', '.join([str(self.season),
                          'Week: %s' % str(self.week),
                          # 'Matchup: %s' % str(self.game_result),
                          # 'Team: %s' % self.team,
                          'Passing Completions: %s' % self.passing_completions,
                          'Passing Attempts: %s' % self.passing_attempts,
                          'Passing Yards: %s' % self.passing_yards,
                          'Passing TD: %s' % self.passing_td,
                          'Passing INT: %s' % self.passing_int,
                          'Rushing Attempts: %s' % self.rushing_attempts,
                          'Rushing Yards: %s' % self.rushing_yards,
                          'Rushing TD: %s' % self.rushing_td,
                          'Targets: %s' % self.receiving_targets,
                          'Receptions: %s' % self.receiving_receptions,
                          'Receiving Yards: %s' % self.receiving_yards,
                          'Receiving TD: %s' % self.receiving_td])

    @staticmethod
    def headers():
        return ', '.join([Season.headers(),
                          '"opponent_city"',
                          '"opponent_name"',
                          '"result"',
                          NflTeam.headers(prefix='player'),
                          '"week"',
                          '"fantasy_points"',
                          '"passing_completions"',
                          '"passing_attempts"',
                          '"passing_yards"',
                          '"passing_td"',
                          '"passing_int"',
                          '"rushing_attempts"',
                          '"rushing_yards"',
                          '"rushing_td"',
                          '"receiving_targets"',
                          '"receiving_receptions"',
                          '"receiving_yards"',
                          '"receiving_td"',
                          '"field_goal_made"',
                          '"field_goal_attempts"',
                          '"extra_point_made"',
                          '"extra_point_attempts"',
                          '"sacks"',
                          '"fumble_recovery"',
                          '"interceptions"',
                          '"defensive_td"',
                          '"points_against"',
                          '"passing_yards_against"',
                          '"rushing_yards_against"',
                          '"safety"',
                          '"kick_return_td"',
                          ])

    def just_the_data(self):
        just_the_data = [self.season.just_the_data()]
        if self.game_result.home_team == self.team:
            just_the_data.append(str(self.game_result.away_team.city))
            just_the_data.append(str(self.game_result.away_team.team_name))
        else:
            just_the_data.append(str(self.game_result.home_team.city))
            just_the_data.append(str(self.game_result.home_team.team_name))
        just_the_data.append(self.result_of_game())
        just_the_data.append(self.team.just_the_data())
        game_stats = [str(self.week),
                      str(self.fantasy_points),
                      str(self.passing_completions),
                      str(self.passing_attempts),
                      str(self.passing_yards),
                      str(self.passing_td),
                      str(self.passing_int),
                      str(self.rushing_attempts),
                      str(self.rushing_yards),
                      str(self.rushing_td),
                      str(self.receiving_targets),
                      str(self.receiving_receptions),
                      str(self.receiving_yards),
                      str(self.receiving_td),
                      str(self.field_goal_made),
                      str(self.field_goal_attempts),
                      str(self.extra_point_made),
                      str(self.extra_point_attempts),
                      str(self.sacks),
                      str(self.fumble_recovery),
                      str(self.interceptions),
                      str(self.defensive_td),
                      str(self.points_against),
                      str(self.passing_yards_against),
                      str(self.rushing_yards_against),
                      str(self.safety),
                      str(self.defensive_td)]
        just_the_data.extend(game_stats)
        return ', '.join(just_the_data)

    def __add__(self, other):
        passing_completions = self.passing_completions + other.passing_completions
        passing_attempts = self.passing_attempts + other.passing_attempts
        passing_yards = self.passing_yards + other.passing_yards
        passing_td = self.passing_td + other.passing_td
        passing_int = self.passing_int + other.passing_int

        rushing_attempts = self.rushing_attempts + other.rushing_attempts
        rushing_yards = self.rushing_yards + other.rushing_yards
        rushing_td = self.rushing_td + other.rushing_td

        receiving_targets = self.receiving_targets + other.receiving_targets
        receiving_receptions = self.receiving_receptions + other.receiving_receptions
        receiving_yards = self.receiving_yards + other.receiving_yards
        receiving_td = self.receiving_td + other.receiving_td

        field_goal_made = self.field_goal_made + other.field_goal_made
        field_goal_attempts = self.field_goal_attempts + other.field_goal_attempts
        extra_point_made = self.extra_point_made + other.extra_point_made
        extra_point_attempts = self.extra_point_attempts + other.extra_point_attempts

        sacks = self.sacks + other.sacks
        fumble_recovery = self.fumble_recovery + other.fumble_recovery
        interceptions = self.interceptions + other.interceptions
        defensive_td = self.defensive_td + other.defensive_td
        points_against = self.points_against + other.points_against
        passing_yards_against = self.passing_yards_against + other.passing_yards_against
        rushing_yards_against = self.rushing_yards_against + other.rushing_yards_against
        safety = self.safety + other.safety
        kick_return_td = self.kick_return_td + other.kick_return_td

        return GameStats(season=self.season,
                         passing_completions=passing_completions,
                         passing_attempts=passing_attempts,
                         passing_yards=passing_yards,
                         passing_td=passing_td,
                         passing_int=passing_int,
                         rushing_attempts=rushing_attempts,
                         rushing_yards=rushing_yards,
                         rushing_td=rushing_td,
                         receiving_targets=receiving_targets,
                         receiving_receptions=receiving_receptions,
                         receiving_yards=receiving_yards,
                         receiving_td=receiving_td,
                         field_goal_made=field_goal_made,
                         field_goal_attempts=field_goal_attempts,
                         extra_point_made=extra_point_made,
                         extra_point_attempts=extra_point_attempts,
                         sacks=sacks,
                         fumble_recovery=fumble_recovery,
                         interceptions=interceptions,
                         defensive_td=defensive_td,
                         points_against=points_against,
                         passing_yards_against=passing_yards_against,
                         rushing_yards_against=rushing_yards_against,
                         safety=safety,
                         kick_return_td=kick_return_td)

    def __mul__(self, other):
        passing_completions = self.passing_completions * other
        passing_attempts = self.passing_attempts * other
        passing_yards = self.passing_yards * other
        passing_td = self.passing_td * other
        passing_int = self.passing_int * other

        rushing_attempts = self.rushing_attempts * other
        rushing_yards = self.rushing_yards * other
        rushing_td = self.rushing_td * other

        receiving_targets = self.receiving_targets * other
        receiving_receptions = self.receiving_receptions * other
        receiving_yards = self.receiving_yards * other
        receiving_td = self.receiving_td * other

        field_goal_made = self.field_goal_made * other
        field_goal_attempts = self.field_goal_attempts * other
        extra_point_made = self.extra_point_made * other
        extra_point_attempts = self.extra_point_attempts * other

        sacks = self.sacks * other
        fumble_recovery = self.fumble_recovery * other
        interceptions = self.interceptions * other
        defensive_td = self.defensive_td * other
        points_against = self.points_against * other
        passing_yards_against = self.passing_yards_against * other
        rushing_yards_against = self.rushing_yards_against * other
        safety = self.safety * other
        kick_return_td = self.kick_return_td * other

        return GameStats(season=self.season,
                         passing_completions=passing_completions,
                         passing_attempts=passing_attempts,
                         passing_yards=passing_yards,
                         passing_td=passing_td,
                         passing_int=passing_int,
                         rushing_attempts=rushing_attempts,
                         rushing_yards=rushing_yards,
                         rushing_td=rushing_td,
                         receiving_targets=receiving_targets,
                         receiving_receptions=receiving_receptions,
                         receiving_yards=receiving_yards,
                         receiving_td=receiving_td,
                         field_goal_made=field_goal_made,
                         field_goal_attempts=field_goal_attempts,
                         extra_point_made=extra_point_made,
                         extra_point_attempts=extra_point_attempts,
                         sacks=sacks,
                         fumble_recovery=fumble_recovery,
                         interceptions=interceptions,
                         defensive_td=defensive_td,
                         points_against=points_against,
                         passing_yards_against=passing_yards_against,
                         rushing_yards_against=rushing_yards_against,
                         safety=safety,
                         kick_return_td=kick_return_td)

    def __rmul__(self, other):
        return self.__mul__(other)

    def result_of_game(self):
        if ((self.team == self.game_result.home_team and
                self.game_result.home_score > self.game_result.away_score) or
                (self.team == self.game_result.away_team and
                 self.game_result.away_score > self.game_result.home_score)):
            return 'Win'
        elif ((self.team == self.game_result.home_team and
                self.game_result.home_score < self.game_result.away_score) or
                (self.team == self.game_result.away_team and
                 self.game_result.away_score < self.game_result.home_score)):
            return 'Loss'
        else:
            return 'Tie'

    def won_game(self):
        return 'w' in self.result_of_game().lower()

    def opponent(self):
        if self.game_result.home_team == self.team:
            return self.game_result.away_team.team_name
        return self.game_result.home_team.team_name

    def average(self, entries):
        avg_passing_completions = int(round(float(self.passing_completions / entries)))
        avg_passing_attempts = int(round(float(self.passing_attempts / entries)))
        avg_passing_yards = int(round(float(self.passing_yards / entries)))
        avg_passing_td = int(round(float(self.passing_td / entries)))
        avg_passing_int = int(round(float(self.passing_int / entries)))

        avg_rushing_attempts = int(round(float(self.rushing_attempts / entries)))
        avg_rushing_yards = int(round(float(self.rushing_yards / entries)))
        avg_rushing_td = int(round(float(self.rushing_td / entries)))

        avg_receiving_targets = int(round(float(self.receiving_targets / entries)))
        avg_receiving_receptions = int(round(float(self.receiving_receptions / entries)))
        avg_receiving_yards = int(round(float(self.receiving_yards / entries)))
        avg_receiving_td = int(round(float(self.receiving_td / entries)))

        avg_field_goal_made = int(round(float(self.field_goal_made / entries)))
        avg_field_goal_attempts = int(round(float(self.field_goal_attempts / entries)))
        avg_extra_point_made = int(round(float(self.extra_point_made / entries)))
        avg_extra_point_attempts = int(round(float(self.extra_point_attempts / entries)))

        avg_sacks = int(round(float(self.sacks / entries)))
        avg_fumble_recovery = int(round(float(self.fumble_recovery / entries)))
        avg_interceptions = int(round(float(self.interceptions / entries)))
        avg_defensive_td = int(round(float(self.defensive_td / entries)))
        avg_points_against = int(round(float(self.points_against / entries)))
        avg_passing_yards_against = int(round(float(self.passing_yards_against / entries)))
        avg_rushing_yards_against = int(round(float(self.rushing_yards_against / entries)))
        avg_safety = int(round(float(self.safety / entries)))
        avg_kick_return_td = int(round(float(self.kick_return_td / entries)))

        return GameStats(season=self.season,
                         passing_completions=avg_passing_completions,
                         passing_attempts=avg_passing_attempts,
                         passing_yards=avg_passing_yards,
                         passing_td=avg_passing_td,
                         passing_int=avg_passing_int,
                         rushing_attempts=avg_rushing_attempts,
                         rushing_yards=avg_rushing_yards,
                         rushing_td=avg_rushing_td,
                         receiving_targets=avg_receiving_targets,
                         receiving_receptions=avg_receiving_receptions,
                         receiving_yards=avg_receiving_yards,
                         receiving_td=avg_receiving_td,
                         field_goal_made=avg_field_goal_made,
                         field_goal_attempts=avg_field_goal_attempts,
                         extra_point_made=avg_extra_point_made,
                         extra_point_attempts=avg_extra_point_attempts,
                         sacks=avg_sacks,
                         fumble_recovery=avg_fumble_recovery,
                         interceptions=avg_interceptions,
                         defensive_td=avg_defensive_td,
                         points_against=avg_points_against,
                         passing_yards_against=avg_passing_yards_against,
                         rushing_yards_against=avg_rushing_yards_against,
                         safety=avg_safety,
                         kick_return_td=avg_kick_return_td)
