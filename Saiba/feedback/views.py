import urllib2, urllib, json
from django.shortcuts import render
from rest_framework.reverse import reverse

def comment_page(request, type):
    id   = request.GET.get('id') or ""
    slug = request.GET.get('slug') or ""
    reply_limit = request.GET.get('reply_limit') or 5

    api_url = reverse('api:api_comment_page', request=request) + "?" + urllib.urlencode({'id':id, 'slug':slug, 'reply_limit': reply_limit, 'type':type})

    result = urllib2.urlopen(api_url).read()
    json_result = json.loads(result)

    args = { 'comments' : json_result['results'], 'u':api_url }

    return render(request, 'feedback/comment_page.html', args)