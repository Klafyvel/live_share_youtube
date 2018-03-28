from urllib.parse import parse_qs
import requests

from django.db import models
from django.shortcuts import reverse

PK_LENGTH = 23
YOUTUBE_INFO_URL = 'http://youtube.com/get_video_info?video_id={}'

class Playlist(models.Model):
    date = models.DateTimeField(verbose_name="date")
    name = models.CharField(
        max_length=255,
        verbose_name="Nom de la playlist"
    )
    last_update = models.DateTimeField(
        verbose_name="Dernière mise à jour"
    )
    last_get = models.DateTimeField(
        verbose_name="Dernière écoute"
    )
    public = models.BooleanField(
        verbose_name="Visible sur la page d'accueil",
        default=True,
    )

    @staticmethod
    def reverse_token(token):
        return token & ((1 << PK_LENGTH) - 1)

    def get_token(self):
        return int(self.date.timestamp()) << PK_LENGTH | self.pk

    def get_absolute_url(self):
        return reverse('player:playlist', kwargs={'token':self.get_token()})

    def __str__(self):
        return "Playlist " + str(self.get_token())


class Link(models.Model):
    token = models.CharField(
        max_length=200,
        verbose_name="Token",
    )
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        verbose_name="Playlist",
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Titre"
    )


    def __str__(self):
        return "Link : " + self.token + " of " + str(self.playlist)

    @classmethod
    def update_titles(cls):
        for o in cls.objects.all():
            response = requests.get(YOUTUBE_INFO_URL.format(o.token))
            o.title = parse_qs(response.content.decode('utf-8'))['title'][0]
            o.save()
