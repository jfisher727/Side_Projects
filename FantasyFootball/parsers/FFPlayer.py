class FFPlayer():

    def set_name(self, name):
        self.name = name

    def set_position(self, position):
        self.position = position

    def set_team(self, team):
        self.team = team

    def set_season(self, season):
        if season.isdigit():
            self.season = int(season)
        else:
            self.season = 0

    def set_week(self, week):
            self.week = week

    def set_passing_completions(self, completions):
        if completions.isdigit():
            self.passing_completions = int(completions)
        else:
            self.passing_completions = 0

    def set_passing_attempts(self, attempts):
        if attempts.isdigit():
            self.passing_attempts = int(attempts)

    def set_passing_yards(self, yards):
        if yards.isdigit():
            self.passing_yards = int(yards)

    def set_passing_td(self, td):
        if td.isdigit():
            self.passing_td = int(td)

    def set_passing_int(self, interceptions):
        if interceptions.isdigit():
            self.passing_int = int(interceptions)

    def set_rushing_attempts(self, attempts):
        if attempts.isdigit():
            self.rushing_attempts = int(attempts)

    def set_rushing_yards(self, yards):
        if yards.isdigit():
            self.rushing_yards = int(yards)

    def set_rushing_td(self, td):
        if td.isdigit():
            self.rushing_td = int(td)

    def set_receiving_targets(self, targets):
        if targets.isdigit():
            self.receiving_targets = int(targets)

    def set_receiving_receptions(self, receptions):
        if receptions.isdigit():
            self.receiving_receptions = int(receptions)

    def set_receiving_yards(self, yards):
        if yards.isdigit():
            self.receiving_yards = int(yards)

    def set_receiving_td(self, td):
        if td.isdigit():
            self.receiving_td = int(td)

    def set_field_goal_made(self, made):
        if made.isdigit():
            self.field_goal_made = int(made)

    def set_field_goal_attempt(self, attempts):
        if attempts.isdigit():
            self.field_goal_attempts = int(attempts)

    def set_extra_point_made(self, made):
        if made.isdigit():
            self.extra_point_made = int(made)

    def set_extra_point_attempt(self, attempts):
        if attempts.isdigit():
            self.extra_point_attempts = int(attempts)

    def set_sacks(self, sacks):
        try:
            self.sacks = int(sacks)
        except ValueError:
            return True

    def set_fumble_recoveries(self, recoveries):
        try:
            self.fumble_recovery = int(recoveries)
        except ValueError:
            return True

    def set_interceptions(self, interceptions):
        try:
            self.interceptions = int(interceptions)
        except ValueError:
            return True

    def set_defensive_td(self, td):
        try:
            self.defensive_td = int(td)
        except ValueError:
            return True

    def set_points_against(self, points):
        try:
            self.points_against = int(points)
        except ValueError:
            return True

    def set_passing_yards_against(self, yards):
        try:
            self.passing_yards_against = float(yards)
        except ValueError:
            return True

    def set_rushing_yards_against(self, yards):
        try:
            self.rushing_yards_against = float(yards)
        except ValueError:
            return True

    def set_safety(self, safety):
        try:
            self.safety = int(safety)
        except ValueError:
            return True

    def set_kick_return_td(self, td):
        try:
            self.kick_return_td = int(td)
        except ValueError:
            return True

    def __str__(self):
        attributes = []
        attributes.append("Name: %s \n" % self.name)
        attributes.append("Position: %s \n" % self.position)
        attributes.append("Team: %s \n" % self.team)
        attributes.append("Season: %s \n" % str(self.season))
        attributes.append("Week: %s \n" % str(self.week))
        if self.position == "QB":
            attributes.append("Passing Completions: %s \n" % str(self.passing_completions))
            attributes.append("Passing Attempts: %s \n" % str(self.passing_attempts))
            attributes.append("Passing Yards: %s \n" % str(self.passing_yards))
            attributes.append("Passing Touchdowns: %s \n" % str(self.passing_td))
            attributes.append("Interceptions: %s \n" % str(self.passing_int))
            attributes.append("Rushing Attempts: %s \n" % str(self.rushing_attempts))
            attributes.append("Rushing Yards: %s \n" % str(self.rushing_yards))
            attributes.append("Rushing Touchdowns: %s \n" % str(self.rushing_td))
        elif self.position == "RB":
            attributes.append("Rushing Attempts: %s \n" % str(self.rushing_attempts))
            attributes.append("Rushing Yards: %s \n" % str(self.rushing_yards))
            attributes.append("Rushing Touchdowns: %s \n" % str(self.rushing_td))
            attributes.append("Receiving Targets: %s \n" % str(self.receiving_targets))
            attributes.append("Receiving Receptions: %s \n" % str(self.receiving_receptions))
            attributes.append("Receiving Yards: %s \n" % str(self.receiving_yards))
            attributes.append("Receiving TD: %s \n" % str(self.receiving_td))
        elif self.position == "WR":
            attributes.append("Receiving Targets: %s \n" % str(self.receiving_targets))
            attributes.append("Receiving Receptions: %s \n" % str(self.receiving_receptions))
            attributes.append("Receiving Yards: %s \n" % str(self.receiving_yards))
            attributes.append("Receiving TD: %s \n" % str(self.receiving_td))
            attributes.append("Rushing Attempts: %s \n" % str(self.rushing_attempts))
            attributes.append("Rushing Yards: %s \n" % str(self.rushing_yards))
            attributes.append("Rushing Touchdowns: %s \n" % str(self.rushing_td))
        elif self.position == "TE":
            attributes.append("Receiving Targets: %s \n" % str(self.receiving_targets))
            attributes.append("Receiving Receptions: %s \n" % str(self.receiving_receptions))
            attributes.append("Receiving Yards: %s \n" % str(self.receiving_yards))
            attributes.append("Receiving TD: %s \n" % str(self.receiving_td))
        elif self.position == "K":
            attributes.append("Field Goal Made: %s \n" % str(self.field_goal_made))
            attributes.append("Field Goal Attempted: %s \n" % str(self.field_goal_attempt))
            attributes.append("Extra Point Made: %s \n" % str(self.extra_point_made))
            attributes.append("Extra Point Attempted: %s \n" % str(self.extra_point_attempt))
        elif self.position == "DEF":
            attributes.append("Sacks: %s \n" % str(self.sacks))
            attributes.append("Fumbles Recovered: %s \n" % str(self.fumble_recovery))
            attributes.append("Interceptions: %s \n" % str(self.interceptions))
            attributes.append("Defensive TD: %s \n" % str(self.defensive_td))
            attributes.append("Points Against: %s \n" % str(self.points_against))
            attributes.append("Passing Yards Against: %s \n" % str(self.passing_yards_against))
            attributes.append("Rushing Yards Against: %s \n" % str(self.rushing_yards_against))
            attributes.append("Safety: %s \n" % str(self.safety))
            attributes.append("Kick Return TD: %s \n" % str(self.kick_return_td))
        else:
            print("Error determining type of position for this player.")

        return "".join(attributes)

    def __init__(self):
        self.name = ""
        self.position = ""
        self.team = ""
        self.season = ""
        self.week = ""

        # QB Stats
        self.passing_completions = 0
        self.passing_attempts = 0
        self.passing_yards = 0
        self.passing_td = 0
        self.passing_int = 0

        # Rushing Stats
        self.rushing_attempts = 0
        self.rushing_yards = 0
        self.rushing_td = 0

        # Receiver Stats
        self.receiving_targets = 0
        self.receiving_receptions = 0
        self.receiving_yards = 0
        self.receiving_td = 0

        # Kicker Stats
        self.field_goal_made = 0
        self.field_goal_attempts = 0
        self.extra_point_made = 0
        self.extra_point_attempts = 0

        # Defense Stats
        self.sacks = 0
        self.fumble_recovery = 0
        self.interceptions = 0
        self.defensive_td = 0
        self.points_against = 0
        self.passing_yards_against = 0
        self.rushing_yards_against = 0
        self.safety = 0
        self.kick_return_td = 0
