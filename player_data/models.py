from django.db import models


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name_first = models.CharField(max_length=50)
    name_last = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name_first} {self.name_last}"
    
    class Meta:
        ordering = ['name_last', 'name_first']


class Batting(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name = "batting",
    )
    year = models.SmallIntegerField()
    runs = models.SmallIntegerField()
    
    class Meta:
        ordering = ['year']


class Pitching(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name = "pitching",
    )
    year = models.SmallIntegerField()
    wins = models.SmallIntegerField()
    
    class Meta:
        ordering = ['year']