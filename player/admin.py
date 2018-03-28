from django.contrib import admin
from .models import Playlist, Link

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
    ordering = ['date']


class LinkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Link, LinkAdmin)
