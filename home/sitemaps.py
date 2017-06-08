from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    #changefreq = "never"

    def items(self):
        return Post.objects.filter(hidden=False)

    def lastmod(self, obj):
        date = obj.date.date()

        if obj.entry:
            date = obj.entry.last_revision().date
        elif obj.image:
            date = obj.image.date
        elif obj.video:
            date = obj.video.date

        return date

    def priority(self, obj):
        if obj.entry:
            return 1
        elif obj.image:
            return 0.8
        elif obj.video:
            return 0.7
