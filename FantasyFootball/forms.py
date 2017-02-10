from django import forms

from .models import Fantasy_League_Settings


class CaptureForm(forms.Form):
    season_choices = (('2016', '2016'), ('2015', '2015'), ('2014', '2014'),
                      ('2013', '2013'), ('2012', '2012'), ('2011', '2011'))
    week_choices = (('ALL', 'ALL'), ('1', '1'), ('2', '2'),
                    ('3', '3'), ('4', '4'), ('5', '5'),
                    ('6', '6'), ('7', '7'), ('8', '8'),
                    ('9', '9'), ('10', '10'), ('11', '11'),
                    ('12', '12'), ('13', '13'), ('14', '14'),
                    ('15', '15'), ('16', '16'), ('17', '17'))
    position_choices = (('ALL', 'ALL'), ('10', 'QB'), ('20', 'RB'),
                        ('30', 'WR'), ('40', 'TE'), ('80', 'K'),
                        ('99', 'DEF'))

    season = forms.ChoiceField(choices=season_choices, label='Season')
    week = forms.ChoiceField(choices=week_choices, label='Week')
    position = forms.ChoiceField(choices=position_choices, label='Position')


class ScheduleForm(forms.Form):
    season_choices = (('2016', '2016'), ('2015', '2015'), ('2014', '2014'),
                      ('2013', '2013'), ('2012', '2012'), ('2011', '2011'))
    week_choices = (('ALL', 'ALL'), ('1', '1'), ('2', '2'),
                    ('3', '3'), ('4', '4'), ('5', '5'),
                    ('6', '6'), ('7', '7'), ('8', '8'),
                    ('9', '9'), ('10', '10'), ('11', '11'),
                    ('12', '12'), ('13', '13'), ('14', '14'),
                    ('15', '15'), ('16', '16'), ('17', '17'))

    season = forms.ChoiceField(choices=season_choices, label='Season')
    week = forms.ChoiceField(choices=week_choices, label='Week')


class PlayerStatsForm(forms.Form):
    team_choices = (('ANY', 'ANY'), ('49ers', '49ers'),
                    ('Cardinals', 'Cardinals'), ('Falcons', 'Falcons'),
                    ('Bears', 'Bears'), ('Bengals', 'Bengals'),
                    ('Bills', 'Bills'), ('Broncos', 'Broncos'),
                    ('Browns', 'Browns'), ('Buccaneers', 'Buccaneers'),
                    ('Chiefs', 'Chiefs'), ('Chargers', 'Chargers'),
                    ('Colts', 'Colts'), ('Cowboys', 'Cowboys'),
                    ('Dolphins', 'Dolphins'), ('Eagles', 'Eagles'),
                    ('Giants', 'Giants'), ('Jaguars', 'Jaguars'),
                    ('Jets', 'Jets'), ('Lions', 'Lions'),
                    ('Packers', 'Packers'), ('Panthers', 'Panthers'),
                    ('Patriots', 'Patriots'), ('Raiders', 'Raiders'),
                    ('Rams', 'Rams'), ('Ravens', 'Ravens'),
                    ('Redskins', 'Redskins'), ('Saints', 'Saints'),
                    ('Seahawks', 'Seahawks'), ('Steelers', 'Steelers'),
                    ('Texans', 'Texans'), ('Titans', 'Titans'),
                    ('Vikings', 'Vikings'))
    position_choices = (('ANY', 'ANY'), ('QB', 'QB'), ('RB', 'RB'),
                        ('WR', 'WR'), ('TE', 'TE'), ('K', 'K'), ('DEF', 'DEF'))

    position = forms.ChoiceField(choices=position_choices, label='Position')
    team = forms.ChoiceField(choices=team_choices, label='Team')
    player_name = forms.CharField(label='Player Name', max_length=100, required=False)


class PlayerPredictionsForm(forms.Form):
    team_choices = (('ANY', 'ANY'), ('49ers', '49ers'),
                    ('Cardinals', 'Cardinals'), ('Falcons', 'Falcons'),
                    ('Bears', 'Bears'), ('Bengals', 'Bengals'),
                    ('Bills', 'Bills'), ('Broncos', 'Broncos'),
                    ('Browns', 'Browns'), ('Buccaneers', 'Buccaneers'),
                    ('Chiefs', 'Chiefs'), ('Chargers', 'Chargers'),
                    ('Colts', 'Colts'), ('Cowboys', 'Cowboys'),
                    ('Dolphins', 'Dolphins'), ('Eagles', 'Eagles'),
                    ('Giants', 'Giants'), ('Jaguars', 'Jaguars'),
                    ('Jets', 'Jets'), ('Lions', 'Lions'),
                    ('Packers', 'Packers'), ('Panthers', 'Panthers'),
                    ('Patriots', 'Patriots'), ('Raiders', 'Raiders'),
                    ('Rams', 'Rams'), ('Ravens', 'Ravens'),
                    ('Redskins', 'Redskins'), ('Saints', 'Saints'),
                    ('Seahawks', 'Seahawks'), ('Steelers', 'Steelers'),
                    ('Texans', 'Texans'), ('Titans', 'Titans'),
                    ('Vikings', 'Vikings'))
    position_choices = (('ANY', 'ANY'), ('QB', 'QB'), ('RB', 'RB'),
                        ('WR', 'WR'), ('TE', 'TE'), ('K', 'K'), ('DEF', 'DEF'))
    season_choices = (('2016', '2016'), ('2015', '2015'), ('2014', '2014'),
                      ('2013', '2013'), ('2012', '2012'), ('2011', '2011'))
    week_choices = (('1', '1'), ('2', '2'),
                    ('3', '3'), ('4', '4'), ('5', '5'),
                    ('6', '6'), ('7', '7'), ('8', '8'),
                    ('9', '9'), ('10', '10'), ('11', '11'),
                    ('12', '12'), ('13', '13'), ('14', '14'),
                    ('15', '15'), ('16', '16'), ('17', '17'))

    position = forms.ChoiceField(choices=position_choices, label='Position')
    team = forms.ChoiceField(choices=team_choices, label='Team')
    season = forms.ChoiceField(choices=season_choices, label='Season')
    week = forms.ChoiceField(choices=week_choices, label='Week')
    fantasy_league_settings = forms.ModelChoiceField(queryset=Fantasy_League_Settings.objects.all().order_by('name'))


class FantasyScoringSelect(forms.Form):
    fantasy_league_settings = forms.ModelChoiceField(queryset=Fantasy_League_Settings.objects.all().order_by('name'))


class FantasyLeagueSettingsForm(forms.ModelForm):
    class Meta:
        model = Fantasy_League_Settings
        fields = '__all__'
        labels = {'name': 'League Name',
                  'roster_size': 'Roster Size',
                  'number_starts': 'Number of Starters',
                  'number_bench': 'Number on Bench',
                  'passing_points_py25': 'Points per 25 passing yards',
                  'passing_interceptions': 'Passing Interceptions',
                  'passing_td': 'Passing TD',
                  'passing_2pt_conversion': '2pt Passing Conversion',
                  'rushing_yards': 'Rushing Yards',
                  'rushing_td': 'Rushing TD',
                  'rushing_2pt_conversion': '2pt Rushing Conversion',
                  'receiving_yards': 'Receiving Yards',
                  'receiving_reception': 'Points per Reception',
                  'receiving_td': 'Receiving TD',
                  'receiving_2pt_conversion': '2pt Receiving Conversion',
                  'field_goal_made': 'Field Goal Made',
                  'field_goal_missed': 'Field Goal Missed',
                  'extra_point_made': 'Extra Point Made',
                  'extra_point_missed': 'Extra Point Missed',
                  'sacks': 'Sacks',
                  'defensive_td': 'Defensive TD',
                  'kick_return_td': 'Kick Returns for TD',
                  'interception': 'Interception',
                  'safety': 'Safety',
                  'fumble_recovery': 'Fumble Recovery',
                  'no_points_allowed': '0 Points Allowed',
                  'one_six_points_allowed': '1-6 Points Allowed',
                  'seven_thirteen_points_allowed': '7-13 Points Allowed',
                  'fourteen_seventeen_points_allowed': '14-17 Points Allowed',
                  'twentyeight_thirtyfour_points_allowed': '24-34 Points Allowed',
                  'thirtyfive_fourtyfive_points_allowed': '35-45 Points Allowed',
                  'fourtysix_plus_points_allowed': '46+ Points Allowed',
                  'under_hundred_total_yards_allowed': 'Less Than 100 Total Yards Allowed',
                  'onehundred_twohundred_total_yards_allowed': '100-199 Total Yards Allowed',
                  'twohundred_threehundred_total_yards_allowed': '200-299 Total Yards Allowed',
                  'threefifty_fourhundred_total_yards_allowed': '350-399 Total Yards Allowed',
                  'fourhundred_fourfifty_total_yards_allowed': '400-449 Total Yards Allowed',
                  'fourfifty_fivehundred_total_yards_allowed': '450-499 Total Yards Allowed',
                  'fivehundred_fivefifty_total_yards_allowed': '500-549 Total Yards Allowed',
                  'fivefifty_plus_total_yards_allowed': '550+ Total Yards Allowed'}
