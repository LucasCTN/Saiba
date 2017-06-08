from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q, Count, Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from .models import Image, Video
from .forms import ImageForm, VideoForm, StaffImageForm, StaffVideoForm
from home.models import Tag
from entry.models import Entry
from saiba import utils, custom_messages
from feedback.models import Action, View

def index(request):
    return render(request, 'entry/index.html')

def image_detail(request, image_id, slug=''):
    image = get_object_or_404(Image, pk=image_id)

    if image.hidden and not request.user.is_staff:
        return redirect('home:index')

    if slug != '-'+image.entry.slug:
        return redirect('gallery:image_detail', image_id=image_id, slug='-'+image.entry.slug)

    utils.register_view(request, image)

    related_images = Image.objects.filter(hidden=False, tags__in=image.tags.all()).\
                        annotate(num_common_tags=Count('pk')).order_by('-num_common_tags').exclude(pk=image.pk)[:5]

    trending_galleries = utils.get_popular_galleries(request)

    type = ContentType.objects.get_for_model(Image)
    views = View.objects.filter(target_content_type=type, target_id=image_id).count()

    context = { 'image'             : image,
                'type'              : 'image',
                'related_images'    : related_images,
                'trending_galleries': trending_galleries,
                'target'            : image,
                'image_slug'        : slug,
                'views'             : views }

    return render(request, 'gallery/image.html', context)

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    if video.hidden and not request.user.is_staff:
        return redirect('home:index')

    utils.register_view(request, video)

    related_videos = Video.objects.filter(hidden=False, tags__in=video.tags.all()).\
                        annotate(num_common_tags=Count('pk')).order_by('-num_common_tags').exclude(pk=video.pk)[:5]

    trending_galleries = utils.get_popular_galleries(request)

    type = ContentType.objects.get_for_model(Video)
    views = View.objects.filter(target_content_type=type, target_id=video_id).count()

    context = { 'video'             : video,
                'type'              : 'video',
                'related_videos'    : related_videos,
                'trending_galleries': trending_galleries,
                'target'            : video,
                'views'             : views,
                'origin'            : get_current_site(request).domain }

    return render(request, 'gallery/video.html', context)

def historic(request, entry_slug):
    trending_galleries = utils.get_popular_galleries(request)
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False)
    return render(request, 'entry/historic.html', {'revisions': revisions, 'entry_name':entry.title })

def revision(request, revision_id):
    trending_galleries = utils.get_popular_galleries(request)
    revision = get_object_or_404(Revision, hidden=False, pk=revision_id)
    return render(request, 'entry/revision.html', {'revision': revision})

def upload_image(request):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        error_messages = []
        valid_form = True
        entry_name = request.POST.get('entry-selected')
        image_form = ImageForm(request.POST or None, request.FILES or None)
        image_entry = Entry.objects.filter(title=entry_name, hidden=False).first()

        if not entry_name:
            valid_form = False
            error_messages.append(custom_messages.get_error_message("entrada", "required"))
        elif not image_entry:
            valid_form = False
            error_messages.append(custom_messages.get_custom_error_message("invalid_entry"))

        if image_entry and image_entry.images_locked:
            valid_form = False
            error_messages.append(custom_messages.get_custom_error_message("locked_images"))

        if not image_form.is_valid():
            error_messages = None

        if image_form.is_valid() and valid_form:
            all_tags = string_tags_to_list(request.POST.get('tags-selected'))
            set_tags = generate_tags(all_tags)

            image = image_form.save(commit=False)
            image.author = request.user
            image.entry = image_entry
            image.save()
            image_form.save_m2m()
            image.tags = Tag.objects.filter(label__in=set_tags)
            image.create_action("4")
            image.save()
            return redirect('gallery:image_detail', image_id=image.pk)

    image_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    image_form.fields['file'].widget.attrs['class'] = 'form-control-file form-file'
    image_form.fields['source'].widget.attrs['class'] = 'form-control form-source'
    image_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    image_form.fields['description'].widget.attrs['class'] = 'form-control form-description'
    image_form.fields['state'].widget.attrs['class'] = 'form-control form-state'

    args = {    "form"      : image_form,
                "errors"    : error_messages }

    return render(request, 'gallery/upload-image.html', args)

def upload_video(request):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        error_messages = []
        entry_name = request.POST.get('entry-selected')
        video_form = VideoForm(request.POST or None)
        video_entry = Entry.objects.filter(title=entry_name, hidden=False).first()

        valid_form = True
        if video_entry and video_entry.videos_locked:
            valid_form = False
            error_messages.append(custom_messages.get_custom_error_message("locked_videos"))

        if video_form.is_valid() and valid_form:
            all_tags = string_tags_to_list(request.POST.get('tags-selected'))
            set_tags = generate_tags(all_tags)

            video = video_form.save(commit=False)
            video.author = request.user
            video.entry = video_entry
            video.save()
            video_form.save_m2m()
            video.tags = Tag.objects.filter(label__in=set_tags)
            video.create_action("5")
            video.save()

            return redirect('gallery:video_detail', video_id=video.id)

    video_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    video_form.fields['media'].widget.attrs['class'] = 'form-control form-media'
    video_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    video_form.fields['description'].widget.attrs['class'] = 'form-control form-description'
    video_form.fields['state'].widget.attrs['class'] = 'form-control form-state'

    return render(request, 'gallery/upload-video.html', {"form": video_form, "errors": error_messages})

def image_edit(request, image_id, slug=''):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        user = request.user
        image = Image.objects.get(pk=image_id)
        entry_name = request.POST.get('entry-selected')
        is_editor = (user == image.author)

        image_dict = model_to_dict(image)
        image_form = ImageForm(request.POST or None, initial=image_dict)

        if user.is_staff:
            image_form = StaffImageForm(request.POST or None, initial=image_dict)

        if image_form.is_valid() and is_editor:
            all_tags = string_tags_to_list(request.POST.get('tags-selected'))
            set_tags = generate_tags(all_tags)

            image_form = ImageForm(request.POST, instance = image)
            
            if user.is_staff:
                image_form = StaffImageForm(request.POST, instance = image)

            image = image_form.save(commit=False)
            image.entry = Entry.objects.filter(title=entry_name, hidden=False).first()
            image.tags = Tag.objects.filter(label__in=set_tags)
            image.create_action("7")
            image.save()
            return redirect('gallery:image_detail', image_id=image.pk)

        context = { "image_form": image_form, "image": image, "user": user }

    image_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    image_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    image_form.fields['source'].widget.attrs['class'] = 'form-control form-source'
    image_form.fields['description'].widget.attrs['class'] = 'form-control form-content'

    return render(request, 'gallery/edit-image.html', context)

def video_edit(request, video_id):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        user = request.user
        video = Video.objects.get(pk=video_id)
        entry_name = request.POST.get('entry-selected')
        is_editor = (user == video.author)
        video_dict = model_to_dict(video)

        request_post = request.POST.copy()

        if request_post:
            request_post["link"] = video.link

        video_form = VideoForm(request_post or None, initial=video_dict)

        if user.is_staff:
            video_form = StaffVideoForm(request_post or None, initial=video_dict)

        if video_form.is_valid() and is_editor:
            all_tags = string_tags_to_list(request.POST.get('tags-selected'))
            set_tags = generate_tags(all_tags)

            video_form = VideoForm(request_post, instance = video)

            if user.is_staff:
                video_form = StaffVideoForm(request_post, instance = video)

            video = video_form.save(commit=False)
            video.entry = Entry.objects.filter(title=entry_name, hidden=False).first()
            video.tags = Tag.objects.filter(label__in=set_tags)
            video.create_action("8")
            video.save()
            return redirect('gallery:video_detail', video_id=video.pk)
        else:
            print video_form.errors
        
        context = { "video_form": video_form, "video": video, "user": user }

    video_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    video_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    video_form.fields['description'].widget.attrs['class'] = 'form-control form-content'

    return render(request, 'gallery/edit-video.html', context)

def string_tags_to_list( tag_string ):
    if(tag_string != None):
        # Splitting all commas
        tags = tag_string.split(",")
        # Removing empty spaces
        tags[:] = (value for value in tags if value != '')
        # Removing all duplicates and returning it (the insertion order it's lost unfortunately)
        return list(set(tags))
    else:
        return ''

def generate_tags( tag_list ):
    # Of the tags written, which one is in database
    db_tags = Tag.objects.filter(label__in=tag_list)

    # Creating a copy of the all tag list
    new_tags = list(tag_list)

    # Removing database tag from the new list (if have any)
    for x in db_tags:
        new_tags[:] = (value for value in new_tags if value != str(x).decode("utf-8"))

    # Inserting in database the new tags
    for tag_name in new_tags:
        Tag.objects.create(label=tag_name, hidden=False)

    # Returning a new list with the database tags and the new created tags
    return list(db_tags) + new_tags