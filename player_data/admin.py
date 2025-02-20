from django.contrib import admin
from .models import Player, Batting, Pitching


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
  list_display = ['name_first', 'name_last']

@admin.register(Batting)
class BattingAdmin(admin.ModelAdmin):
  list_display = ['player', 'year', 'org_abbreviation']

@admin.register(Pitching)
class PitchingAdmin(admin.ModelAdmin):
  list_display = ['year', 'wins']