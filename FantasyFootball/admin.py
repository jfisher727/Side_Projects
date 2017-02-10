from django.contrib import admin

from .models import Player
from .models import Season
from .models import Weekly_Stats


class SeasonInLine(admin.TabularInline):
    model = Season


class Weekly_StatsInLine(admin.TabularInline):
    model = Weekly_Stats


class Player_Admin(admin.ModelAdmin):
    fields = ['player', 'position', 'season']
    inlines = [SeasonInLine]


class Season_Admin(admin.ModelAdmin):
    fields = ['player', 'team', 'season']
    inlines = [Weekly_StatsInLine]


admin.site.register(Season, Season_Admin)
# admin.site.register(Player, Player_Admin)
