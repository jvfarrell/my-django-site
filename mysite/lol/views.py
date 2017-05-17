from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from lol.models import Summoner, Stats, Champion
from mysite.forms import SummonerForm
import requests, json
import pandas as pd
import lol.api_config as config

# Set up code

#champion info names
key = config.api_key
url_champ_info = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key='+key
championInfo = requests.get(url_champ_info)
champ_dict = {}
for champion in championInfo.json()['data']:
    champ_dict[championInfo.json()['data'][champion]['id']] = championInfo.json()['data'][champion]['name']


def getChampSimpleName(champID):
    return champ_dict[champID].lower().replace(' ', '').replace('\'', '').replace('.','')

champ_ids = {}
for champ_id in champ_dict:
    s = getChampSimpleName(champ_id)
    champ_ids[s] = champ_id


def getSummonerChampLevel(tempChampID, summID):
    url = 'https://na.api.pvp.net/championmastery/location/NA1/player/'+str(summID)+'/champion/'+str(tempChampID)+'?api_key='+key
    getChampExp = requests.get(url)
    if getChampExp.status_code == 200:
        #has experience
        return getChampExp.json()['championLevel']
    else:
        return 0

# Create your views here

def search_form(request):
    return render(request, 'lol_search_form.html')


def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            summoners = Summoner.objects.filter(name__icontains=q)
            return render(request, 'lol_search_results.html', {'summoners': summoners, 'query': q})
    return render(request, 'lol_search_form.html',
                  {'errors': errors})


def summoner_landing(request):
    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get('summoner_name')

            return HttpResponseRedirect('/summoner/'+name)
    else:
        form = SummonerForm()
        return render(request, 'summoner_landing_page.html', {'form': form})


def summoner(request, sum_name):
    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get('summoner_name')

            return HttpResponseRedirect('/summoner/'+name)
    else:
        name = str(sum_name)
        form = SummonerForm(
            initial={'summoner_name': name}
        )
        plain_name = name.replace(' ', '')
        key = config.api_key #api key
        #name_requested_formatted = name.replace('+', '%20')
        url = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + plain_name + '?api_key=' + key
        response = requests.get(url)
        data = response.json()

        # get Summoner ID and name
        sumName = ''
        for name in data:
            sumName = name
        sumID = data[sumName]['id']
        icon_id = data[sumName]['profileIconId']
        sumID = str(sumID)
        icon_url = 'http://ddragon.leagueoflegends.com/cdn/7.9.1/img/profileicon/'+str(icon_id)+'.png'

        # Get summoner Rank
        url = 'https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/' + sumID + '?api_key=' + key
        rank = requests.get(url)
        textRank = ''
        if rank.status_code == 200:
            for player in rank.json()[sumID][0]['entries']:
                if player['playerOrTeamId'] == sumID:
                    textRank = rank.json()[sumID][0]['tier'].capitalize() + ' ' + player['division'] + ' - ' + 'LP: ' + str(
                        player['leaguePoints'])
        else:
            textRank = 'Unranked'

        # Get Ranked Stats
        url = 'https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + sumID + '/ranked?season=SEASON2017&api_key=' + key
        rankedStats = requests.get(url)
        if rankedStats.status_code == 200:
            # get all champion ranked stats by champ id and put into DF
            personal_champ_ranked_stats = {}
            for champ in rankedStats.json()['champions']:
                if (champ['id'] == 0):
                    continue
                personal_champ_ranked_stats[champ['id']] = champ['stats']

            df_personal_champ_ranked_stats = pd.DataFrame(personal_champ_ranked_stats)
            df_personal_champ_ranked_stats = df_personal_champ_ranked_stats.T
            df_personal_champ_ranked_stats['KDA'] = (
                                                        df_personal_champ_ranked_stats.totalAssists + df_personal_champ_ranked_stats.totalChampionKills) / df_personal_champ_ranked_stats.totalDeathsPerSession
            df_personal_champ_ranked_stats[
                'winRatio'] = df_personal_champ_ranked_stats.totalSessionsWon / df_personal_champ_ranked_stats.totalSessionsPlayed
            df_personal_champ_ranked_stats = df_personal_champ_ranked_stats.T

            # get top ranked champs
            top_champs = df_personal_champ_ranked_stats.T.sort_values(by='totalSessionsPlayed', ascending=False)[0:5]

            champ_list = []
            # show relevant stats for champs
            for c in top_champs.T:
                name = champ_dict[c]
                games_played = top_champs.T[c].totalSessionsPlayed
                kda = top_champs.T[c].KDA
                win_ratio = '{percent:.1%}'.format(percent=top_champs.T[c].winRatio)
                mastery = getSummonerChampLevel(c, sumID)
                champ_url = 'http://ddragon.leagueoflegends.com/cdn/7.9.1/img/champion/'+name+'.png'
                list_item = {'name': name, 'games_played': games_played, 'kda': kda, 'win_ratio': win_ratio,
                             'mastery': mastery, 'champ_url': champ_url}
                champ_list.append(list_item)

        return render(request, 'summoner_lookup.html', {'summoner_name': sum_name, 'rank': textRank, 'icon_url': icon_url,
                                                        'champ_list': champ_list, 'form': form})
