from urllib.parse import urlparse
import django.utils.timezone as timezone

from django import forms

from player.models import Playlist, Link

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name']

    def is_valid(self):
        self.instance.date = timezone.now()
        self.instance.last_get = timezone.now()
        self.instance.last_update = timezone.now()
        return super().is_valid()

class LinkForm(forms.Form):
    url = forms.URLField(label="URL de la piste à ajouter")

    def get_token(self):
        p=urlparse(self.cleaned_data['url'])
        print(p.query)
        return [i for i in p.query.split('&') if i and i[0]=='v'][0].split('=')[-1]

