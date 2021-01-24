from django.db import models

class Player(models.Model):
    player_id = models.IntegerField()
    first_name = models.CharField(max_length = 50, blank = True, null = True)
    last_name = models.CharField(max_length = 50, blank = True, null = True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

