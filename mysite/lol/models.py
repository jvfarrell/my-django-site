# Create your models here.
from django.db import models


class Summoner(models.Model):
    name = models.CharField(max_length=50)
    summoner_id = models.CharField(max_length=50)
    profile_icon_id = models.CharField(max_length=10)
    summoner_level = models.IntegerField()
    lookup_name = models.CharField(max_length=50)
    op_gg_profile = models.URLField(blank=True)
    rank = models.CharField(max_length=20)

    def __str__(self):
        return u'%s %s' % (self.name, self.rank)

    class Meta:
        ordering = ['name']


class Champion(models.Model):
    name = models.CharField(max_length=30)
    champ_id = models.IntegerField()

    def __init__(self, name, champ_id):
        self.name = name
        self.champ_id = champ_id

    def __str__(self):
        return self.name


class ChampInfo(models.Model):
    name = models.ForeignKey(Champion)
    lore = models.CharField(max_length=5000)
    passive = models.CharField(max_length=300)
    q_skill = models.CharField(max_length=300)
    w_skill = models.CharField(max_length=300)
    e_skill = models.CharField(max_length=300)
    r_skill = models.CharField(max_length=300)
    attack_damage = models.DecimalField(max_digits=5, decimal_places=2)
    ability_power = models.DecimalField(max_digits=5, decimal_places=2)
    health = models.DecimalField(max_digits=5, decimal_places=2)
    move_speed = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Stats(models.Model):
    champ_id = models.ForeignKey(Champion)
    summoner_id = models.ForeignKey(Summoner)
    mastery = models.IntegerField()
    games_played = models.IntegerField()
    kda = models.DecimalField(max_digits=4, decimal_places=2)
    win_ratio = models.DecimalField(max_digits=5, decimal_places=2)

    def __init__(self, champ_id, summoner_id, mastery, games_played, kda, win_ratio):
        self.champ_id = champ_id
        self.summoner_id = summoner_id
        self.mastery = mastery
        self.games_played = games_played
        self.kda = kda
        self.win_ratio = win_ratio

    def __str__(self):
        return u'%s %s %s' % (self.champ_id, self.summoner_id, self.mastery)