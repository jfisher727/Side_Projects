from django.db import models

from .player import Player


class Season(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, editable=False)
    season = models.IntegerField()

    def __str__(self):
        return ", ".join([str(self.player),
                          'Season: %s' % self.season])

    def just_the_data(self):
        return ', '.join([self.player.just_the_data(),
                          str(self.season)])

    @staticmethod
    def headers():
        return ", ".join([Player.headers(),
                          '"season"'])
