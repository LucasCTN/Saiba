# -*- coding: utf-8 -*-
import copy
import imghdr
import json
import urllib
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from ipware.ip import get_ip
from rest_framework.reverse import reverse

import saiba.settings
from api.views import TrendingDetail
from feedback.models import View
from django.http import HttpRequest


def send_activation_email(request, user, token):
    '''Sends a email to the user with a token. It uses the settings.py email.'''
    title = "Saiba - Ative sua conta"
    email_activation_url = request.\
                            build_absolute_uri(reverse('home:email_activation',
                                                       kwargs={'username_slug': user.profile.slug,
                                                               'token_code': token.code}))
    message = '''Olá, {0}.
Para poder se autenticar, você precisa ativar sua conta, clicando no seguinte link:
    
{1}

Caso você não tenha se registrado, ou esta mensagem é um engano, ignore-a.

Obrigado!

Equipe Saiba.
{2}
'''.format(user.username, email_activation_url,
           get_current_site(request).domain)

    send_mail(subject=title, message=message, from_email=saiba.settings.EMAIL_HOST_USER,
              recipient_list=[user.email], fail_silently=False)

def is_valid_direction(direction):
    return int(direction) in [-1, 0, 1]

def get_popular_galleries(request):
    new_request = copy.copy(request)
    new_request.method = "GET" #This is horrible

    trending_galleries = TrendingDetail.as_view()(new_request, "gallery").data
    result = trending_galleries[:5]
    return result

def string_tags_to_list( tag_string ):
    if(tag_string != None):
        # Splitting all commas
        tags = tag_string.split(",")
        verified_tags = []

        # Removing empty and only one space tags
        for tag in tags:
            tag = tag.strip()
            # If the tag is valid, include on the 'verified_tags' list
            if tag != '' and tag != ' ':
                verified_tags.append(tag)

        # Removing all duplicates and returning it (the insertion order it's lost unfortunately)
        return list(set(verified_tags))
    else:
        return ''

def generate_tags( tag_list, tag_database ):
    # Of the tags written, which one is in database
    tags_from_database = tag_database.objects.filter(label__in=tag_list)

    # Creating a copy of the all tag list
    new_tags = list(tag_list)

    # Removing database tag from the new list (if have any)
    for x in tags_from_database:
        new_tags[:] = (value for value in new_tags if value != str(x).decode("utf-8"))

    # Inserting in database the new tags
    for tag_name in new_tags:
        tag_database.objects.create(label=tag_name, hidden=False)

    # Returning a new list with the database tags and the new created tags
    return list(tags_from_database) + new_tags

def save_image_link( link ):
    accepted_image_files = [ 'bmp', 'gif', 'jpeg', 'png' ]

    # Trying to access the image url and storing the content. If succeeds continue the operations or else set the content to None
    try:
        content = ContentFile(urllib.request.urlopen(link).read())

        # Verify if the content captured is a valid image format based on 'accepted_image_files'
        valid_file = imghdr.what(content) in accepted_image_files
    except:
        return (None, None)

    if content and valid_file:
        # Getting the name of the file splitting the url and capturing the last part (ex. blabla.com/hello.png => ['bla.com', 'hello.png'] => 'hello.png')
        name = link.split('/')[-1]

        # Returning the image and the original name
        return (name, content)

# It return the date on string format (20 de Março de 2017) if the date is valid.
# Returns empty ('') if the date was not inserted.
# And return False when the date is invalid.
def verify_and_format_date( day, month, year ):
    if day.isdigit():
        day = int(day)
        
        if day < 1 or day > 31:
            day = 0
    else:
        day = 0

    if month.isdigit():
        month = int(month)
        
        if month < 1 or month > 12:
            month = 0
    else:
        month = 0

    if year.isdigit():
        year = int(year)
        
        if year < 0:
            year = 0
    else:
        year = 0

    month_list = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    if date_is_before_datetime(day, month, year, datetime.now()):
        if day != 0 and month != 0 and year != 0:
            return str(day) + " de " + str(month_list[month]) + " de " + str(year)
        elif day == 0 and month != 0 and year != 0:
            return str(month_list[month]) + " de " + str(year)
        elif day == 0 and month == 0 and year != 0:
            return str(year)
        elif day == 0 and month == 0 and year == 0:
            return ''
        else:
            return False
    else:
        return False

def date_is_before_datetime( day, month, year, datetime ):
    input_date = datetime

    if day != 0:
        input_date = input_date.replace(day=day)

    if month != 0:
        input_date = input_date.replace(month=month)

    if year != 0:
        input_date = input_date.replace(year=year)

    if (datetime - input_date).days >= 0:
        return True
    else:
        return False

def register_view(request, target):
    bot_terms = ["bot", "crawl", "crawler", "slurp", "spider", "link", "checker", "script", "robot", "discovery", "preview"]
    bot_names = ['Googlebot','Slurp','Twiceler','msnbot','KaloogaBot','YodaoBot','Baiduspider','googlebot','Speedy Spider','DotBot']

    is_a_bot = False

    for bot_term in (bot_terms + bot_names):
        is_a_bot = bot_term in request.META['HTTP_USER_AGENT']

        if is_a_bot:
            break

    # if none of these terms or names are on the HTTP_USER_AGENT so it's not a bot.
    if not is_a_bot:
        content_type = ContentType.objects.get_for_model(target)

        current_ip = get_ip(request)

        # here the waiting time before another view is set.
        time_threshold = datetime.now() - timedelta(hours=3)

        already_viewed = View.objects.filter(target_id=target.id, target_content_type=content_type, ip=current_ip, date__gt=time_threshold) or None

        if not already_viewed:
            if request.user.is_authenticated():
                user = request.user
            else:
                user = None

            new_view = View.objects.create( author      = user,
                                            target      = target, 
                                            ip          = current_ip, 
                                            user_agent  = request.META['HTTP_USER_AGENT'],
                                            session     = request.session.session_key or None)
