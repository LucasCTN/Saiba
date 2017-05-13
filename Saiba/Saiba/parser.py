import re
import urllib, json, textile
from bs4 import BeautifulSoup

youtube_video_width = "640"
youtube_video_height = "390"
origin = "localhost"

def generate_tweet(tweet_match):
    tweet_url = tweet_match.group(1)
    url = "https://publish.twitter.com/oembed?url=" + tweet_url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data["html"]

def generate_trends(term_match, initial_date = "today", final_date = "3-m"):
    terms = term_match.group(1)
    terms = [item.strip() for item in terms.split(',')]

    result = '<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/760_RC01/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("TIMESERIES", {"comparisonItem":['

    counter = 0

    for term in terms:
        counter += 1
        result += '{' + '"keyword":"{}","geo":"","time":"{} {}"'.format(term, initial_date, final_date) + '}'
        if counter != len(terms):
            result += ","

    result += '],"category":0,"property":""}, {"exploreQuery":"q='

    counter = 0
    for term in terms:
        counter += 1

        term = urllib.quote_plus(term)

        result += term
        if counter != len(terms):
            result += ","

    result += '","guestPath":"https://www.google.com.br:443/trends/embed/"}); </script>'
    return result

def generate_youtube_video(yt_match):
    video_url = yt_match.group(1)
    result = '<iframe id="ytplayer" type="text/html" width={} height={} src="http://www.youtube.com/embed/{}?origin={}" frameborder="0"></iframe>'.format(youtube_video_width, youtube_video_height, video_url, origin)
    return result

def resize_image(image_match):
    image_match = re.sub(r' =(\d+)x(\d+)(.+)\/>', r'\3width="\1" height="\2"/>', image_match.group(0))
    image = re.sub(r' =(center|right|left)(.+)\/>', r'\2 align="\1"/>', image_match)
    return image

def parse(text):
    '''Parse the text with textile, removes meta and script tags and apply custom rules.'''
    soup = BeautifulSoup(text, "html.parser")
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('meta')]

    text = soup.text
    text = textile.textile(text)

    text = re.sub(r'\?{twitter}\((.+?)\)'   , generate_tweet        , text) # Capturing Twitter embeds
    text = re.sub(r'\?{trends}\((.+?)\)'    , generate_trends       , text) # Capturing Google Trends embeds
    text = re.sub(r'\?{youtube}\((.+?)\)'   , generate_youtube_video, text) # Capturing YouTube embeds
    return text