# -*- coding: utf-8 -*-
from embed_video.backends import VideoBackend

class FacebookBackend(VideoBackend):
    re_detect = re.compile(r'(?:facebook|fb).com')

    #re_code = re.compile(r'(?:facebook|fb).com(?:/|%2F)(.+|)(?:/|%2F|)(?:videos|video.php?v=)(?:/|%2F|)([0-9]+)')
    re_code = re.compile(r'facebook.com(?:/|%2F)(.+)(?:/|%2F)videos(?:/|%2F)([0-9]+)')

    allow_https = False
    pattern_url = '{protocol}://play.myvideo.com/c/{code}/'
    pattern_thumbnail_url = '{protocol}://thumb.myvideo.com/c/{code}/'

    template_name = 'embed_video/custombackend_embed_code.html'  # added in v0.9