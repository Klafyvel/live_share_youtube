import requests
import json

from django.db import models, migrations, transaction
YOUTUBE_INFO_URL = 'http://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={}&format=json'

def gen_title(apps, schema_editor):
    Link = apps.get_model('player', 'Link')
    for o in Link.objects.all():
        response = requests.get(YOUTUBE_INFO_URL.format(o.token))
        q = json.loads(response.content.decode('utf-8'))
        try:
            o.title = q['title']
        except KeyError:
            o.delete()
        else:
            o.save()


class Migration(migrations.Migration):
    dependencies = [
        ('player', '0004_playlist_public'),
    ]
    atomic = False

    operations = [
        migrations.AddField(
            model_name='link',
            name='title',
            field= models.CharField(null=True, max_length=200, verbose_name="Titre"),
        ),
        migrations.RunPython(gen_title),
        migrations.AlterField(
            model_name='link',
            name='title',
            field= models.CharField(max_length=255, verbose_name="Titre"),
        ),
    ]
