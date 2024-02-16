from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.http import JsonResponse
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from requests import post
from .models import SpotifyToken
from datetime import datetime, timedelta
from spotdl import Spotdl
# Create your views here.

SPOTIFY_CLIENT_ID = "2f7fb0d053fd41d19455705c92ea0135"
SPOTIFY_CLIENT_SECRET = "f1a587f0b84a4f409816b8b14cd2a397"
REDIRECT_URI = "http://mdfazal.pythonanywhere.com/redirect"
SCOPE = 'user-read-playback-state user-modify-playback-state user-read-currently-playing web-playback user-top-read'
sf = None

def authorize(request):
    sf = SpotifyOAuth(SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    sf.get_access_token(check_cache=False) #get code from uri the parse it in spotify_callback
    
    return redirect("http://localhost:3000")
    # print(request.session['user'])
    # return JsonResponse(request.session["user"])

# def get_user_info(request):
#     try:
#         user_data = request.session['user']
#         return JsonResponse(user_data)
#     except:
#         return HttpResponseRedirect("http://127.0.0.1:8000/spotify/authorize")
    
    
def spotify_callback(request):
    sf = SpotifyOAuth(SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET, scope=SCOPE, redirect_uri="http://mdfazal.pythonanywhere.com/redirect", show_dialog=True)
    code = sf.parse_response_code(url=request.build_absolute_uri())
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    sp = spotipy.Spotify(auth=access_token)
    # print(dict(sp.current_user()))

    current_datetime = datetime.now()
    expire_datetime = current_datetime + timedelta(seconds=expires_in)

    if SpotifyToken.objects.filter(user=sp.current_user()['id']).count() == 0:
        SpotifyToken.objects.create(user=sp.current_user()['id'], refresh_token=refresh_token, access_token=access_token, expires_in=expire_datetime, token_type=token_type)
    else:
        SpotifyToken.objects.filter(user=sp.current_user()['id']).update(user=sp.current_user()['id'], refresh_token=refresh_token, access_token=access_token, expires_in=expire_datetime, token_type=token_type)
    
    request.session['user'] = dict(sp.current_user())

    return HttpResponseRedirect("http://localhost:3000/user/" + request.session['user']['id'])

def update_token_in_db(request, response,user_id):
    print(response["access_token"])
    SpotifyToken.objects.filter(user=user_id).update(access_token=response["access_token"], expires_in=datetime.fromtimestamp(response["expires_at"]), refresh_token=response["refresh_token"])
    return None

def refresh(request, user_id):
    print("here at refresth ", user_id)
    refresh_token = SpotifyToken.objects.get(user=user_id).refresh_token
    sf = SpotifyOAuth(SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    response =  sf.refresh_access_token(refresh_token=refresh_token)
    print("######################################")
    print(response)
    update_token_in_db(request, response, user_id)
    return None

def retrieve_working_access_token(request, user_id):
    access_token = SpotifyToken.objects.get(user=user_id).access_token
    dummy_query = "abc"
    # refresh(request, user_id)  #refresh token if expired
    # return SpotifyToken.objects.get(user=user_id).access_token
    try:
        sp = spotipy.Spotify(auth=access_token)
        result = sp.search(dummy_query, limit=1)
    except Exception as e:
        if("status: 401" in str(e)):
            refresh(request, user_id)  #refresh token if expired
            access_token = SpotifyToken.objects.get(user=user_id).access_token
    return access_token


def search(request, query, user_id):
    
    # try:

    # user_id = request.session.get("user_id")
    # print("here", user_id, request.session)
    access_token = retrieve_working_access_token(request, user_id)
    # except:
    #     return HttpResponseRedirect("/spotify/authorize")

    sp = spotipy.Spotify(auth=access_token)
    result = sp.search(query, limit=20)

    return JsonResponse(result)


def user_playlists(request, user_id, offset=0, limit=50):
    access_token = retrieve_working_access_token(request, user_id)
    sp = spotipy.Spotify(auth=access_token)
    result = sp.current_user_playlists(limit, offset)
    return JsonResponse(result)

def user_saved_albums(request, user_id, offset=0, limit=50):
    access_token = retrieve_working_access_token(request, user_id)
    sp = spotipy.Spotify(auth=access_token)
    result = sp.current_user_saved_albums(limit, offset)
    return JsonResponse(result)

def user_top_tracks(request, user_id, offset=0, limit=20):
    access_token = retrieve_working_access_token(request, user_id)
    sp = spotipy.Spotify(auth=access_token)
    result = sp.current_user_top_tracks(limit=limit, offset=offset)
    return JsonResponse(result)

def initiate_playback(request, track_uri=None, user_id=None):
    access_token = retrieve_working_access_token(request, user_id)
    sp = spotipy.Spotify(auth=access_token)
    sp.start_playback(uris=[track_uri])
    return HttpResponse("400")


def spdl(request, track_uri):
    spotify_url = "https://open.spotify.com/track/" + track_uri.split(':')[-1]
    s = Spotdl(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    songs = s.search([spotify_url])
    data=s.downloader.search(songs[0])
    url = s.downloader.audio_providers[0].get_download_metadata(data)["url"]
    return JsonResponse({"ddl": url})

# def create_stream(to_stream_url):
#     import ffmpeg_streaming
#     from ffmpeg_streaming import Formats
#     audio = ffmpeg_streaming.input(to_stream_url)
#     print(audio)
#     hls = audio.hls(Formats.)

def get_user_info(request, user_id):
    access_token = retrieve_working_access_token(request, user_id)
    sp = spotipy.Spotify(auth=access_token)
    result = sp.current_user()
    return JsonResponse(result)

def get_recommendations(request, user_id, tracks):
    tracks = tracks.split(",")
    access_token = retrieve_working_access_token(request, user_id)
    sp = spotipy.Spotify(auth=access_token)
    result = sp.recommendations(seed_tracks=tracks)
    return JsonResponse(result)


