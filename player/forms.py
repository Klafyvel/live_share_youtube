from urllib.parse import urlparse, parse_qs

import django.utils.timezone as timezone
from django import forms

from player.models import Playlist, Link


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'public']

    def is_valid(self):
        self.instance.date = timezone.now()
        self.instance.last_get = timezone.now()
        self.instance.last_update = timezone.now()
        return super().is_valid()

class LinkForm(forms.Form):
    url = forms.URLField(label="URL de la piste à ajouter")

    def get_token(self):
        p=urlparse(self.cleaned_data['url'])
        p = parse_qs(p.query)
        return p['v'][0]


