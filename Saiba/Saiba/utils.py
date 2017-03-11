import copy
from api.views import TrendingDetail

def is_valid_direction(direction):
    return int(direction) in [-1, 0, 1]

def get_trending_entries(request):
    new_request = copy.copy(request)
    new_request.method = "GET" #This is horrible

    trending_entries = TrendingDetail.as_view()(new_request, "entry").data
    result = trending_entries[:5]
    return result

def get_popular_galleries(request):
    new_request = copy.copy(request)
    new_request.method = "GET" #This is horrible

    trending_galleries = TrendingDetail.as_view()(new_request, "gallery").data
    result = trending_galleries[:5]
    return result