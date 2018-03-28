import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import django.utils.timezone as timezone

from player.models import Playlist, Link
from player.forms import PlaylistForm, LinkForm

def new_playlist(request):
    p = PlaylistForm(request.POST or None)
    if p.is_valid():
        playlist = p.save()
        return redirect(playlist.get_absolute_url())
    return render(request, 'form.html', {
        'form':p,
        'validate':'Créer',
        'title':'Nouvelle playlist'
    })


@csrf_exempt
def get_list(request, token):
    p = get_object_or_404(Playlist, pk=Playlist.reverse_token(token))
    p.last_get = timezone.now()
    p.save()

    d = {'tokens':[], 'updated':False}
    last_up = p.last_update.timestamp()
    last_sync = (int(request.GET['last_sync'])/1000)

    if p.last_update.timestamp() >= int(request.GET['last_sync'])/1000:
        d['updated'] = True
        d['tokens'] = [l.token for l in p.link_set.all()]
    return HttpResponse(json.dumps(d), content_type='application/json')


@csrf_exempt
def add_link(request, token):
    p = get_object_or_404(Playlist, pk=Playlist.reverse_token(token))
    l = LinkForm(request.POST or None)
    if l.is_valid():
        p.last_update = timezone.now()
        p.save()
        yt_token = l.get_token()
        link = Link()
        link.token = yt_token
        link.playlist = p
        link.save()
        return HttpResponse('Ok')
    return render(request, 'form_inline.html', {
        'form':l,
        'validate':'Ajouter'
    })


def remove_link(request, pk):
    l = get_object_or_404(Link, pk=pk)
    l.delete()
    return HttpResponse('Ok')


def playlist(request, token):
    p = get_object_or_404(Playlist, pk=Playlist.reverse_token(token))
    add_link_form = LinkForm()
    return render(request, 'player/playlist.html', {
        'playlist':p,
        'form':add_link_form
    })


def all_playlist(request):
    p = Playlist.objects.filter(public=True).order_by('date')
    return render(request, 'player/all_list.html', {'lists':p})
