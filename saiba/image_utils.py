# -*- coding: utf-8 -*-
import copy
import imghdr
import json
import os
import urllib
from datetime import datetime
from urllib.request import urlopen

from django.core.files import File
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from rest_framework.reverse import reverse


def save_image_link( link ):
    link = str(link)
    accepted_image_files = [ 'bmp', 'gif', 'jpeg', 'png' ]

    # Trying to access the image url and storing the content. If succeeds continue the operations or else set the content to None
    try:
        content = ContentFile(urlopen(link).read())

        # Verify if the content captured is a valid image format based on 'accepted_image_files'
        valid_file = imghdr.what(content) in accepted_image_files
    except:
        return (None, None)

    if content and valid_file:
        # Getting the name of the file splitting the url and capturing the last part (ex. blabla.com/hello.png => ['bla.com', 'hello.png'] => 'hello.png')
        name = link.split('/')[-1]

        # Returning the image and the original name
        return (name, content)

def download_external_image(url):
    '''Downloads an image from the url and returns, in order, the file name and the actual file.'''

    try:
        img_file = urlopen(url).read()
    except:
        return (None, None)

    file_name = get_random_string(length=15) + os.path.splitext(url)[1]
    return (file_name, img_file)
