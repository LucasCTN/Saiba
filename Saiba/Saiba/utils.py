from rest_framework.reverse import reverse
import urllib, urllib2, json

def is_valid_direction(direction):
    return int(direction) in [-1, 0, 1]

def get_trending_entries(request):
    entry_trending_url = reverse('api:api_trending', request=request) + "?type=entry"

    entry_trending_result = urllib2.urlopen(entry_trending_url).read()
    trending_entries = json.loads(entry_trending_result)

    return trending_entries[:5]

def get_popular_galleries(request):
    gallery_trending_url = reverse('api:api_trending', request=request) + "?type=gallery"

    gallery_trending_result = urllib2.urlopen(gallery_trending_url).read()
    trending_galleries = json.loads(gallery_trending_result)

    return trending_galleries[:5]