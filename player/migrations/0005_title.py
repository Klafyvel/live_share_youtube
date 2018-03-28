from urllib.parse import parse_qs
import requests

from django.db import models, migrations, transaction
YOUTUBE_INFO_URL = 'http://youtube.com/get_video_info?video_id={}'

def gen_title(apps, schema_editor):
    Link = apps.get_model('player', 'Link')
    for o in Link.objects.all():
        response = requests.get(YOUTUBE_INFO_URL.format(o.token))
        q = parse_qs(response.content.decode('utf-8'))
        try:
            o.title = q['title'][0]
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
