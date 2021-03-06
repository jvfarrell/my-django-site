# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-03 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChampInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lore', models.CharField(max_length=5000)),
                ('passive', models.CharField(max_length=300)),
                ('q_skill', models.CharField(max_length=300)),
                ('w_skill', models.CharField(max_length=300)),
                ('e_skill', models.CharField(max_length=300)),
                ('r_skill', models.CharField(max_length=300)),
                ('attack_damage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ability_power', models.DecimalField(decimal_places=2, max_digits=5)),
                ('health', models.DecimalField(decimal_places=2, max_digits=5)),
                ('move_speed', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('champ_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mastery', models.IntegerField()),
                ('games_played', models.IntegerField()),
                ('kda', models.DecimalField(decimal_places=2, max_digits=4)),
                ('win_ratio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('champ_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lol.Champion')),
            ],
        ),
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('summoner_id', models.CharField(max_length=50)),
                ('profile_icon_id', models.CharField(max_length=10)),
                ('summoner_level', models.IntegerField()),
                ('lookup_name', models.CharField(max_length=50)),
                ('op_gg_profile', models.URLField()),
                ('rank', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='stats',
            name='summoner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lol.Summoner'),
        ),
        migrations.AddField(
            model_name='champinfo',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lol.Champion'),
        ),
    ]
