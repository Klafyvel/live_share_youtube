from django.db import models

PK_LENGTH = 23

class Playlist(models.Model):
    date = models.DateTimeField(verbose_name="date")

    @staticmethod
    def reverse_token(token):
        return token & ((1 << PK_LENGTH) - 1)

    def get_token(self):
        return int(self.date.timestamp()) << PK_LENGTH | self.pk

    def get_absolute_url(self):
        pass

    def __str__(self):
        return "Playlist " + str(self.get_token())


class Link(models.Model):
    url = models.URLField(verbose_name="Lien")
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        verbose_name="Playlist",
    )

    def __str__(self):
        return "Link : " + self.url + " of " + str(self.playlist)
