from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=235)
    position = models.CharField(max_length=10)

    def __str__(self):
        return ', '.join(['Name: %s' % self.name,
                          'Position: %s' % self.position])

    def just_the_data(self):
        return ', '.join([str(self.name),
                          str(self.position)])

    @staticmethod
    def headers():
        return ', '.join(['"name"', '"position"'])
