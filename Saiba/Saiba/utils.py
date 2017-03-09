from rest_framework.reverse import reverse
from api.views import TrendingDetail

def is_valid_direction(direction):
    return int(direction) in [-1, 0, 1]

def get_trending_entries(request):
    trending_entries = TrendingDetail.as_view()(request, "entry").data
    return trending_entries[:5]

def get_popular_galleries(request):
    trending_galleries = TrendingDetail.as_view()(request, "gallery").data
    return trending_galleries[:5]