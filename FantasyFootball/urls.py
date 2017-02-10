from django.conf.urls import url

from . import views

app_name = 'fantasyfootball'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^matchups/(?P<season_number>[0-9]+)/$', views.season_matchups, name='season_matchups'),
    url(r'^boxscores/(?P<matchup_id>[0-9]+)/$', views.matchup_boxscore, name='matchup_boxscore'),
    url(r'^player_stats_request/$', views.get_player_stats, name='player_stats'),
    url(r'^update_request/$', views.update_entries, name='update_entries'),
    url(r'^league_settings/$', views.all_league_settings_display, name='all_league_settings'),
    url(r'^league_settings/(?P<settings_id>[0-9]+)/$', views.league_settings_display, name='league_settings_display'),
    url(r'^league_settings_request/$', views.get_league_settings_request, name='league_settings_request'),
    url(r'^player_stats/(?P<player_id>[0-9]+)/$', views.player_details, name='player_details'),
    url(r'^season_stats/(?P<player_id>[0-9]+)/(?P<season_id>[0-9]+)/$', views.season_details, name='season_details'),
    url(r'^player_predictions/$', views.get_player_prediction, name='player_predictions'),
]
