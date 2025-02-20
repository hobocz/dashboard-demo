from django.db import models


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name_first = models.CharField(max_length=50)
    name_use = models.CharField(max_length=50)
    name_last = models.CharField(max_length=50)
    team = models.CharField(max_length=3)
    birth_date = models.DateField()
    height_feet = models.PositiveSmallIntegerField(null=True)
    height_inches = models.PositiveSmallIntegerField(null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    throws = models.CharField(max_length=1)
    bats = models.CharField(max_length=1)
    primary_position = models.CharField(max_length=1, null=True)

    def __str__(self):
        return f"{self.name_first} {self.name_last}"
    
    class Meta:
        ordering = ['name_last', 'name_first']
        indexes = [
            models.Index(fields=['name_last', 'name_first']),
            models.Index(fields=['team']),
        ]


class Batting(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name = "batting",
    )
    year = models.PositiveSmallIntegerField()
    league = models.CharField(max_length=2, null=True)
    org_abbreviation = models.CharField(max_length=3)
    plate_appearances = models.PositiveSmallIntegerField()
    at_bats = models.PositiveSmallIntegerField()
    games = models.PositiveSmallIntegerField()
    games_started = models.PositiveSmallIntegerField()
    runs = models.PositiveSmallIntegerField()
    hits = models.PositiveSmallIntegerField()
    doubles = models.PositiveSmallIntegerField()
    triples = models.PositiveSmallIntegerField()
    home_runs = models.PositiveSmallIntegerField()
    bases_on_balls = models.PositiveSmallIntegerField()
    strikeouts = models.PositiveSmallIntegerField()
    sacrifices = models.PositiveSmallIntegerField()
    sacrifice_flies = models.PositiveSmallIntegerField()
    stolen_bases = models.PositiveSmallIntegerField()
    caught_stealing = models.PositiveSmallIntegerField()
    
    class Meta:
        ordering = ['player', 'year']
        indexes = [
            models.Index(fields=['org_abbreviation']),
            models.Index(fields=['runs']),
        ]


class Pitching(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name = "pitching",
    )
    year = models.PositiveSmallIntegerField()
    league = models.CharField(max_length=2, null=True)
    org_abbreviation = models.CharField(max_length=3)
    games = models.PositiveSmallIntegerField()
    games_started = models.PositiveSmallIntegerField()
    complete_games = models.PositiveSmallIntegerField()
    games_finished = models.PositiveSmallIntegerField()
    innings_pitched = models.FloatField()
    wins = models.PositiveSmallIntegerField()
    losses = models.PositiveSmallIntegerField()
    saves = models.PositiveSmallIntegerField()
    total_batters_faced = models.PositiveSmallIntegerField()
    at_bats = models.PositiveSmallIntegerField()
    hits = models.PositiveSmallIntegerField()
    doubles = models.PositiveSmallIntegerField()
    triples = models.PositiveSmallIntegerField()
    home_runs = models.PositiveSmallIntegerField()
    bases_on_balls = models.PositiveSmallIntegerField()
    strikeouts = models.PositiveSmallIntegerField()
    
    class Meta:
        ordering = ['year']
        indexes = [
            models.Index(fields=['org_abbreviation']),
            models.Index(fields=['wins']),
        ]