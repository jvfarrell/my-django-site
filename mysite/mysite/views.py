from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from mysite.forms import ContactForm, SummonerForm
from django.core.mail import send_mail
import datetime, requests, json, random, os
import mysite.quotes
import lol.api_config as config

import datetime


def hello(request):
    return HttpResponse("Hello world")


def resume(request):
    return render(request, 'resume.html')


def home(request):
    qotd = mysite.quotes.get_random_quote()
    return render(request, 'homepage.html', {'daily_quote': qotd})


def my_homepage_view(request):
    return HttpResponse("Welcome to the tmp Homepage!")


def nfl_analytics(request):
    return render(request, 'nfl_analytics.html')

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'hours_ahead.html', {'hour_offset': offset, 'next_time': dt})


def display_meta(request):
    values = request.META.items()
    ##values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def videos_page(request):
    return render(request, 'youtube_links.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['jvictorfarrell@gmail.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(
            initial={'subject': 'I love your site!'}
        )
    return render(request, 'contact_form.html', {'form': form})

def summoner(request):
    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            key = config.api_key
            cd['summoner_name']
            nameRequestedFormatted = cd['summoner_name'].replace(' ', '%20')
            url = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + nameRequestedFormatted + '?api_key=' + key
            response = requests.get(url)
            data = response.json()
            sumName = ''
            for name in data:
                sumName = name
            sumID = data[sumName]['id']
            sumID = str(sumID)

            return render(request, 'summoner_form.html', {'form': form, 'sum_name': sumName})
    else:
        form = ContactForm(
            initial={'summoner_name': 'Malibu Schnapps'}
        )
    return render(request, 'summoner_form.html', {'form': form})