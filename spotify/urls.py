from django.urls import path
from . import views

urlpatterns = [
    path('authorize', views.authorize),
    path('redirect', views.spotify_callback),
    path('user/<user_id>', views.get_user_info),
    path('user/<user_id>/search/<str:query>', views.search),
    path('user/<user_id>/playlists/<int:limit>/<int:offset>', views.user_playlists),
    path('user/<user_id>/albums/<int:limit>/<int:offset>', views.user_saved_albums),  #haven't made a ui for this yet
    path('user/<user_id>/playback/<track_uri>', views.initiate_playback),
    path('user/<user_id>/refreshkey',views.refresh),
    path('spdl/<track_uri>', views.spdl),
    path('user/<user_id>/recommendations/<tracks>', views.get_recommendations),
    path('user/<user_id>/mytoptracks/<int:limit>/<int:offset>', views.user_top_tracks)
]
