from django.urls import path
from . import views

app_name = "player"
urlpatterns = [
    path('<int:token>', views.playlist, name='playlist'),
    path('remove/<int:pk>', views.remove_link, name='remove-link'),
    path('<int:token>/add', views.add_link, name='add'),
    path('<int:token>/list', views.get_list, name='list'),
    path('new', views.new_playlist, name='new'),
    path('', views.all_playlist, name='all'),
]
