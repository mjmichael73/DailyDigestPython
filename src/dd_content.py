import csv
import random
import os
from urllib import request
import json
import datetime
import tweepy
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_LAT = os.getenv('WEATHER_LAT')
WEATHER_LNG = os.getenv('WEATHER_LNG')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={WEATHER_LAT}&lon={WEATHER_LNG}&appid={WEATHER_API_KEY}"


def get_random_quote(quotes_file="quotes.csv"):
    try:
        with open(quotes_file) as csv_file:
            quotes = [
                {'author': line[0], 'quote': line[1]}
                for line in csv.reader(csv_file, delimiter='|')
            ]
    except Exception as e:
        quotes = [
            {'author': 'Mojtaba Michael', 'quote': 'You can do it.'}
        ]
    return random.choice(quotes)


def get_weather_forecast():
    try:
        data = json.load(request.urlopen(WEATHER_URL))
        forecast = {
            'city': data['city']['name'],
            'country': data['city']['country'],
            'periods': list()
        }
        for period in data['list'][0:9]:
            forecast['periods'].append({
                'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                'temp': round(period['main']['temp']),
                'description': period['weather'][0]['description'].title(),
                'icon': f"https://operweathermap.org/img/wn/{period['weather']}"
            })
        return forecast
    except Exception as e:
        return e


def get_twitter_trends(woeid=23424977):
    try:
        auth = tweepy.AppAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
        return tweepy.API(auth).get_place_trends(woeid)[0]['trends']
    except Exception as e:
        return e


def get_wikipedia_article():
    try:
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {
            'title': data['title'],
            'extract': data['extract'],
            'url': data['content_urls']['desktop']['page']
        }
    except Exception as e:
        return e


if __name__ == '__main__':
    print(f" - Random quote is: {get_random_quote()}")
    print(f" - Weather is: {get_weather_forecast()}")
    print(f" - Twitter trends are: {get_twitter_trends()}")
    print(f" - Wikipedia article is: {get_wikipedia_article()}")
