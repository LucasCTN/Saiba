import math
from .models import Comment, Vote
from entry.models import Entry
from gallery.models import Image, Video
from profile.models import Profile
from django.contrib.contenttypes.models import ContentType

def create_comment(id = None, type = None, user = None, content = None):
    """Creates a comment for a target."""
    target = find_target(id, type)
    comment = Comment.objects.create(target = target, author = user, content = content)
    comment.save()

def get_target_parent_comments(id = None, type = None):
    """Returns a queryset of comments associated with the target."""
    target = find_target(id, type)
    target_type = ContentType.objects.get_for_model(target)
    target_id = target.id

    comments = Comment.objects.filter(target_content_type = target_type, target_id = target_id, parent = None)
    return comments

def get_target_comment_page(id = None, type = None, page = 1, limit = 10):
    """Returns a queryset of comments associated with the target."""
    target = find_target(id, type)
    target_type = ContentType.objects.get_for_model(target)
    target_id = target.id

    comments = Comment.objects.filter(target_content_type = target_type, target_id = target_id, parent = None)[::-1]
    return get_page(comments, page, limit)

def get_comment_children(comment = None): #is this still needed?
    """Returns a queryset of replies associated with the comment."""
    return comment.children

def get_target_page_count(id = None, type = None, page_limit = 10): #is this still needed?
    """Returns the number of pages by counting the comments."""
    target = find_target(id, type)
    target_type = ContentType.objects.get_for_model(target)
    target_id = target.id

    comments = Comment.objects.filter(target_content_type = target_type, target_id = target_id, parent = None).count()
    page_count = math.ceil(float(comments) / page_limit)
    return page_count

def vote_target(id = None, type = None, user = None, direction = 0):
    """
    Votes a target.
    
    direction   -- can only be 0, 1 or -1 (null, up or down)
    """
    target = find_target(id, type)
    vote = Vote.objects.create(target = target, author = user)
    vote.save()

def get_votes_from_target(id = None, type = None):
    """Returns a queryset of votes associated with the target."""
    target = find_target(id, type)
    target_type = ContentType.objects.get_for_model(target)
    target_id = target.id

    votes = Vote.objects.filter(target_content_type = target_type, target_id = target_id)
    return votes

def find_target(id = None, type = None):
    """Returns a target based on the type."""
    types_map = { "comment": Comment, "image": Image, "video": Video, "entry": Entry, "profile": Profile }
    type = types_map[type]

    target = type.objects.get(id = id)

    return target

def get_page(full_list, page, page_length):
    return full_list[(page-1)*page_length:][:page_length]

def convert_type(type_name):
    type_map = {"comment":Comment, "entry":Entry, "image":Image}
    target_type = ContentType.objects.get_for_model(type_map[type_name])
    return target_type