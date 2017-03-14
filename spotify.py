import requests

GET_ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'

# https://developer.spotify.com/web-api/get-artist/
def get_artist(artist_id):
	url = GET_ARTIST_ENDPOINT.format(id=artist_id)
	resp = requests.get(url)
	return resp.json()

# https://developer.spotify.com/web-api/search-item/
def search_by_artist_name(name):
	myparams = {'type': 'album,artist,playlist,track'}
	myparams['q'] = name
	myparams['limit'] = 6
	resp = requests.get(SEARCH_ENDPOINT, params=myparams)
	return resp.json()

# https://developer.spotify.com/web-api/get-artists-top-tracks/
def get_artist_top_tracks(artist_id, country='US'):
	url = TOP_TRACKS_ENDPOINT.format(id=artist_id)
	myparams = {'country': country}
	resp = requests.get(url, params=myparams)
	return resp.json()

def get_sth_by_time(time):
	resp = requ
	return 
