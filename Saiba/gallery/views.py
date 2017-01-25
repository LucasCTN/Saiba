from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q, Count, Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from .models import Image, Video
from .forms import ImageForm, VideoForm
from home.models import Tag
from entry.models import Entry

def index(request):
    return render(request, 'entry/index.html')

def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    related_images = Image.objects.filter(hidden=False, tags__in=image.tags.all()).\
                        annotate(num_common_tags=Count('pk')).order_by('-num_common_tags').exclude(pk=image.pk)[:5]

    context = { 'image'         : image,
                'type'          : 'image',
                'id'            : image.pk,
                'related_images': related_images}    

    return render(request, 'gallery/image.html', context)

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    related_videos = Video.objects.filter(hidden=False, tags__in=video.tags.all()).\
                        annotate(num_common_tags=Count('pk')).order_by('-num_common_tags').exclude(pk=video.pk)[:5]

    context = { 'video'         : video,
                'type'          : 'video',
                'id'            : video.pk,
                'related_videos': related_videos}

    return render(request, 'gallery/video.html', context)

def historic(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False)
    return render(request, 'entry/historic.html', {'revisions': revisions, 'entry_name':entry.title})

def revision(request, revision_id):
    revision = get_object_or_404(Revision, hidden=False, pk=revision_id)
    return render(request, 'entry/revision.html', {'revision': revision})

def upload_image(request):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        image_form = ImageForm(request.POST or None)

        if image_form.is_valid():
            image_form = ImageForm(request.POST, request.FILES)
            image = image_form.save(commit=False)
            image.author = request.user
            image.save()
            image_form.save_m2m()
            return render(request, 'gallery/image.html', {'image': image})

    image_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    image_form.fields['file'].widget.attrs['class'] = 'form-control-file form-file'
    image_form.fields['source'].widget.attrs['class'] = 'form-control form-source'
    image_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    image_form.fields['description'].widget.attrs['class'] = 'form-control form-description'
    image_form.fields['state'].widget.attrs['class'] = 'form-control form-state'

    return render(request, 'gallery/upload-image.html', {"form": image_form})

def upload_video(request):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        video_form = VideoForm(request.POST or None)
        entry_name = request.POST.get('entry-selected')

        if video_form.is_valid():
            all_tags = string_tags_to_list(request.POST.get('tags-selected'))
            set_tags = generate_tags(all_tags)

            video_form = VideoForm(request.POST, request.FILES)
            video = video_form.save(commit=False)
            video.author = request.user
            video.entry = Entry.objects.filter(title=entry_name, hidden=False).first()
            video.save()
            video_form.save_m2m()
            video.tags = Tag.objects.filter(label__in=set_tags)
            video.save()
            return redirect('gallery:video_detail', video_id=video.id)

    video_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    video_form.fields['link'].widget.attrs['class'] = 'form-control form-link'
    video_form.fields['state'].widget.attrs['class'] = 'form-control form-state'
    video_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    video_form.fields['description'].widget.attrs['class'] = 'form-control form-description'
    video_form.fields['state'].widget.attrs['class'] = 'form-control form-state'

    return render(request, 'gallery/upload-video.html', {"form": video_form})

def image_edit(request, image_id):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        user = request.user
        image = Image.objects.get(pk=image_id)
        is_editor = (user == image.author)

        print "ALLALAL"
        print image
        print model_to_dict(image)

        image_form = ImageForm(request.POST or None, request.FILES, initial=model_to_dict(image))

        print image_form.errors

        if image_form.is_valid() and is_editor:
            all_tags = string_tags_to_list(request.POST.get('tags-selected'))
            set_tags = generate_tags(all_tags)

            print "maximum LEL"
            print request.POST.get('tags-selected')

            image_form = ImageForm(request.POST, request.FILES, instance = image)
            image = image_form.save(commit=False)
            image.tags = Tag.objects.filter(label__in=set_tags)
            image.save()
            return redirect('gallery:image_detail', image_id=image.pk)

        context = { "image_form": image_form, "image":image, "user":user }

    image_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    image_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    image_form.fields['source'].widget.attrs['class'] = 'form-control form-source'
    image_form.fields['description'].widget.attrs['class'] = 'form-control form-content'

    return render(request, 'gallery/edit-image.html', context)

def search_tags(request):
    if request.GET:
        search_text = request.GET.get('q')
    else:
        search_text = ''

    if search_text != '':
        tag_search_result = Tag.objects.filter(label__contains=search_text, hidden=False)[:5]
    else:
        tag_search_result = None

    args = { 'tag_search_result' : tag_search_result }

    return render(request, 'gallery/search_tag.html', args)

def search_entries(request):
    if request.GET:
        search_text = request.GET.get('q')
    else:
        search_text = ''

    if search_text != '':
        entry_search_result = Entry.objects.filter(title__contains=search_text, hidden=False)[:5]
    else:
        entry_search_result = None

    args = { 'entry_search_result' : entry_search_result }

    return render(request, 'gallery/search_entry.html', args)

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
