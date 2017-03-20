# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse
import urllib, urllib2, json
from django.core.files import File
from django.core.files.base import ContentFile
from datetime import datetime
import imghdr

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
        content = ContentFile(urllib2.urlopen(link).read())

        # Verify if the content captured is a valid image format based on 'accepted_image_files'
        valid_file = imghdr.what(content) in accepted_image_files
    except:
        return (None, None)

    if content and valid_file:
        # Getting the name of the file splitting the url and capturing the last part (ex. blabla.com/hello.png => ['bla.com', 'hello.png'] => 'hello.png')
        name = link.split('/')[-1]

        # Returning the image and the original name
        return (name, content)

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
        else:
            return ""
    else:
        return ""

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