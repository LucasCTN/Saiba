from .models import Comment, Vote, Reply
from entry.models import Entry
from gallery.models import Image, Video
from django.contrib.contenttypes.models import ContentType

def create_comment(id = None, type = None, user = None, content = None):
    """Creates a comment for a target."""
    target = find_target(id, type)
    comment = Comment.objects.create(target = target, author = user, content = content)
    comment.save()

def get_comments_from_target(id = None, type = None):
    """Returns a queryset of comments associated with the target."""
    target = find_target(id, type)
    target_type = ContentType.objects.get_for_model(target)
    target_id = target.id

    comments = Comment.objects.filter(target_content_type = target_type, target_id = target_id)
    return comments

def get_replies_from_comment(comment = None):
    """Returns a queryset of replies associated with the comment."""    
    replies = Reply.objects.filter(comment = comment)
    return replies

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
    types_map = { "comment": Comment, "image": Image, "video": Video, "entry": Entry }
    type = types_map[type]

    target = type.objects.get(id = id)

    return target