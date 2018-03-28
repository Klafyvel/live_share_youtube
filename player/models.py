from django.db import models
from django.shortcuts import reverse

PK_LENGTH = 23

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

    def __str__(self):
        return "Link : " + self.token + " of " + str(self.playlist)
