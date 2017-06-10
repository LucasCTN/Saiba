# -*- coding: utf-8 -*-
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from embed_video.backends import VideoBackend
import re

class FacebookBackend(VideoBackend):
    """
    Backend for Facebook URLs.
    """
    re_detect = re.compile(
        r'^(http(s)?://)?(www\.|m\.)?(?:facebook|fb)(\.com)?\/.*', re.I
    )

    re_code = re.compile(
        r'''(fb|facebook)\.com              # match facebook's domains
        (/|%2F)
        (?!plugins/video.)                  # exclude the plugins
        (?P<page>(?:.+|))                   # capture the page name
        (/videos|video.php\?v|%2Fvideos)
        (/|%2F|=)
        (?P<code>[0-9]+)                    # capturing the video code
        ''', re.I | re.X)

    #pattern_url = '{protocol}://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com%2F{page}%2Fvideos%2F{code}%2F&width={width}&show_text=false&height={height}&appId'
    pattern_url = '{protocol}://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com%2F{page}%2Fvideos%2F{code}%2F&show_text=false&appId'
    pattern_thumbnail_url = '{protocol}://graph.facebook.com/{code}/picture/type={resolution}'

    resolutions = [
        'small',
        'normal',
        'album',
        'large',
        'square',
    ]

    template_name = 'gallery/facebookbackend_embed_code.html'  # added in v0.9

    @cached_property
    def width(self):
        """
        :rtype: str
        """
        return self.info.get('width')

    @cached_property
    def height(self):
        """
        :rtype: str
        """
        return self.info.get('height')

    def get_page(self):
        """
        Returns page name matched from given url by :py:data:`re_code`.
        :rtype: str
        """
        match = self.re_code.search(self._url)
        if match:
            return match.group('page')

    @property
    def page(self):
        """
        Page of video.
        """
        return self.get_page()

    def get_url(self):
        """
        Returns URL folded from :py:data:`pattern_url` and parsed code.
        """

        url = self.pattern_url.format(code=self.code, protocol=self.protocol, page=self.page)
        url += '?' + self.query.urlencode() if self.query else ''
        return mark_safe(url)