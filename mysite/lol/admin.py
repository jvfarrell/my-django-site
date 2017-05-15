from django.contrib import admin
from .models import Summoner, Stats, Champion, ChampInfo

class SummonerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank')
    search_fields = ('name', 'rank')

class ChampionAdmin(admin.ModelAdmin):
    list_display = ('name', 'champ_id')
    list_filter = ('name',)
    ordering = ('-name',)

class StatsAdmin(admin.ModelAdmin):
    list_display = ('summoner_id', 'champ_id', 'mastery', 'games_played', 'kda', 'win_ratio')
    list_filter = ('summoner_id', 'champ_id')
    ordering = ('-summoner_id',)

# Register your models here.
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Champion, ChampionAdmin)
admin.site.register(Stats, StatsAdmin)
admin.site.register(ChampInfo)
