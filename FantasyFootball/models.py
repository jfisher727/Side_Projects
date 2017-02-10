from django.db import models

# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=235)
    position = models.CharField(max_length=10)

    def __str__(self):
        return "".join(['Name: %s \n' % self.name,
                        'Position: %s \n' % self.position,
                        'Player ID: %d \n' % self.id])


class Season(models.Model):
    team = models.CharField(max_length=10)
    season = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return "".join([str(self.player),
                        'Team: %s \n' % self.team,
                        'Season: %s \n' % str(self.season)])


class Matchup(models.Model):
    home_team = models.CharField(max_length=30)
    home_score = models.IntegerField(null=True)
    away_team = models.CharField(max_length=30)
    away_score = models.IntegerField(null=True)
    season = models.IntegerField()
    week = models.IntegerField()

    def __str__(self):
        return "".join(['Season: %s \n' % str(self.season),
                        'Week Number: %s \n' % str(self.week),
                        'Away Team: %s, Score: %s \n' % (self.away_team, str(self.away_score)),
                        'Home Team: %s, Score: %s \n' % (self.home_team, str(self.home_score))])


class Weekly_Stats(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    matchup = models.ForeignKey(Matchup, on_delete=models.CASCADE, null=True)
    week = models.IntegerField(null=True)

    passing_completions = models.IntegerField()
    passing_attempts = models.IntegerField()
    passing_yards = models.IntegerField()
    passing_td = models.IntegerField()
    passing_int = models.IntegerField()

    rushing_attempts = models.IntegerField()
    rushing_yards = models.IntegerField()
    rushing_td = models.IntegerField()

    receiving_targets = models.IntegerField()
    receiving_receptions = models.IntegerField()
    receiving_yards = models.IntegerField()
    receiving_td = models.IntegerField()

    field_goal_made = models.IntegerField()
    field_goal_attempts = models.IntegerField()
    extra_point_made = models.IntegerField()
    extra_point_attempts = models.IntegerField()

    sacks = models.IntegerField()
    fumble_recovery = models.IntegerField()
    interceptions = models.IntegerField()
    defensive_td = models.IntegerField()
    points_against = models.IntegerField()
    passing_yards_against = models.IntegerField()
    rushing_yards_against = models.IntegerField()
    safety = models.IntegerField()
    kick_return_td = models.IntegerField()

    def __str__(self):
        return "".join([str(self.season),
                        'Week: %s \n' % str(self.week),
                        # 'Matchup: %s \n' % str(self.matchup),
                        'Passing Completions: %d \n' % self.passing_completions,
                        'Passing Attempts: %d \n' % self.passing_attempts,
                        'Passing Yards: %d \n' % self.passing_yards,
                        'Passing TD: %d \n' % self.passing_td,
                        'Passing INT: %d \n' % self.passing_int,
                        'Rushing Attempts: %d \n' % self.rushing_attempts,
                        'Rushing Yards: %d \n' % self.rushing_yards,
                        'Rushing TD: %d \n' % self.rushing_td,
                        'Targets: %d \n' % self.receiving_targets,
                        'Receptions: %d \n' % self.receiving_receptions,
                        'Receiving Yards: %d \n' % self.receiving_yards,
                        'Receiving TD: %d \n' % self.receiving_td])

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

        return Weekly_Stats(season=self.season,
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
                            kick_return_td=kick_return_td
                            )

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

        return Weekly_Stats(season=self.season,
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
                            kick_return_td=avg_kick_return_td
                            )


class Fantasy_League_Settings(models.Model):
    name = models.CharField(max_length=30)
    roster_size = models.IntegerField(null=True)
    number_starters = models.IntegerField(null=True)
    number_bench = models.IntegerField(null=True)

    passing_points_py25 = models.IntegerField()
    passing_interception = models.IntegerField()
    passing_td = models.IntegerField()
    passing_2pt_conversion = models.IntegerField()

    rushing_yards = models.DecimalField(max_digits=2, decimal_places=1)
    rushing_td = models.IntegerField()
    rushing_2pt_conversion = models.IntegerField()

    receiving_yards = models.DecimalField(max_digits=2, decimal_places=1)
    receiving_reception = models.DecimalField(max_digits=2, decimal_places=1)
    receiving_td = models.IntegerField()
    receiving_2pt_conversion = models.IntegerField()

    field_goal_made = models.IntegerField()
    field_goal_missed = models.IntegerField()
    extra_point_made = models.IntegerField()
    extra_point_missed = models.IntegerField()

    sacks = models.IntegerField()
    defensive_td = models.IntegerField()
    kick_return_td = models.IntegerField()
    interception = models.IntegerField()
    safety = models.IntegerField()
    fumble_recovery = models.IntegerField()

    no_points_allowed = models.IntegerField()
    one_six_points_allowed = models.IntegerField()
    seven_thirteen_points_allowed = models.IntegerField()
    fourteen_seventeen_points_allowed = models.IntegerField()
    twentyeight_thirtyfour_points_allowed = models.IntegerField()
    thirtyfive_fourtyfive_points_allowed = models.IntegerField()
    fourtysix_plus_points_allowed = models.IntegerField()

    under_hundred_total_yards_allowed = models.IntegerField()
    onehundred_twohundred_total_yards_allowed = models.IntegerField()
    twohundred_threehundred_total_yards_allowed = models.IntegerField()
    threefifty_fourhundred_total_yards_allowed = models.IntegerField()
    fourhundred_fourfifty_total_yards_allowed = models.IntegerField()
    fourfifty_fivehundred_total_yards_allowed = models.IntegerField()
    fivehundred_fivefifty_total_yards_allowed = models.IntegerField()
    fivefifty_plus_total_yards_allowed = models.IntegerField()

    def to_string(self):
        return "".join(["Name: %s \n" % self.name,
                        "Roster Size: %d \n" % self.roster_size,
                        "Starter Count: %d \n" % self.number_starters,
                        "Bench Count: %d \n" % self.number_bench,
                        "Points per 25 yards passing: %d \n" % self.passing_points_py25,
                        "Points per interception: %d \n" % self.passing_interception,
                        "Points per Passing TD: %d \n" % self.passing_td,
                        "Passing 2PT Conversion: %d \n" % self.passing_2pt_conversion,
                        "Points per rushing yard: %d \n" % self.rushing_yards,
                        "Points per rushing TD: %d \n" % self.rushing_td,
                        "Rushing 2PT Conversion: %d \n" % self.rushing_2pt_conversion])

    def __str__(self):
        return self.name


class Fantasy_League_Team(models.Model):
    fantasy_league = models.ForeignKey(Fantasy_League_Settings, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=50)
    owner = models.CharField(max_length=20)


class Fantasy_League_Player(models.Model):
    this_weeks_stats = models.ForeignKey(Weekly_Stats, on_delete=models.CASCADE)
    fantasy_owner = models.ForeignKey(Fantasy_League_Team, on_delete=models.CASCADE)
