#!/usr/bin/env python3
import os
import json
import pytumblrhaha.pytumblr
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, render_template_string
import github_flask
import spotify

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , CM1.py


# Load default config and override config from an environment variable
app.config.update(dict(SECRET_KEY="development key"))

# setup github-flask
github = github_flask.GithubAuth("fd7e54a1f4ac9becf832", "fff5546dbb5b35cee777bc779aec918b06348c09", "session_key")


@app.route("/")
def index():
	if "user_id" in session:
		return redirect(url_for("user"))
	print("HAHAHAHAH")
	return render_template("login.html")


@github.access_token_getter
def token_getter():
	if "access_token" in session:
		return session["access_token"]

@app.route("/github-callback")
@github.authorized_handler
def authorized(access_token):
	print(access_token)
	a = access_token[b'access_token'].decode("utf8")
	if not access_token:
		return redirect(url_for("index"))
	session["user_id"] = 1
	session["access_token"] = a
	return redirect(url_for("user"))

@app.route("/login")
def login():
	return github.authorize()

@app.route("/logout")
def logout():
	session.pop("user_id", None)
	session.pop("access_token", None)
	return redirect(url_for("index"))

@app.route("/user")
def user():
#	print("\n\n\n\nahahaha\n\n\n\n\n")
#	client = pytumblrhaha.pytumblr.TumblrRestClient("5jZTWDFTTkQKj8YY3Fst3HM9gojVOg0BtSRp43vNmRbA3CFotm")
#	client = pytumblrhaha.pytumblr.TumblrRestClient("Oa6rsvJagrgeqnHeEFHjWIreo53HBMyHZpnOS9KnoUhmebx5PK")
	client = pytumblrhaha.pytumblr.TumblrRestClient("SzUodhnLgnKjoWdC44Va45u0KXmdUoexPLuqlR3EkWEjp0Sip6")
	resp1, content1 = github.get_resource("user/repos")
	resp2, content2 = github.get_resource("user")
	json_data = json.loads(content1.decode("utf8"))
	user = json.loads(content2.decode("utf8"))
#	print(user)
	username = user["login"]
	location = user["location"]
	repos = []
	p = []
	tumblrs = {}
	info = {"name": None, "pushed_at": None, "created_at": None, "updated_at": None}
	tum_info = {"url": None, "post_url": None, "description": None, "excerpt": None, "slug": None, "blog_name": None, "title": None, "summary": None, "tags": None, "publisher": None, "short_url": None, "audio_url": None, "audio_source_url": None, "permalink_url": None, "source_title": None, "audio_type": None, "track_name": None}
	for j in json_data:
		temp = tum_info.copy()
		info["name"] = j["name"]
		info["pushed_at"] = j["pushed_at"]
		info["created_at"] = j["created_at"][:10]
		info["updated_at"] = j["updated_at"]
		tumblr_data1 = client.tagged(info["created_at"][5:7]+" music", limit=20)
		tumblr_data2 = client.tagged(info["created_at"][:4]+" music", limit=20)
		tumblr_data3 = client.tagged(info["created_at"][:4]+" concert", limit=20)
		tumblr_data4 = client.tagged(info["created_at"][5:7]+" concert", limit=20)
		tumblr_data_mix = tumblr_data1 + tumblr_data2 + tumblr_data3 + tumblr_data4
		tumblr_data = random.sample(tumblr_data_mix, 2)
		tumblrs[info["name"]] = []
		"""
		for blog in tumblr_data:
			temp = tum_info.copy()
			for tag in blog:
				if tag in temp:
					temp[tag] = blog[tag]
			tumblrs[info["name"]].append(temp)
		"""
		for blog in tumblr_data:
			temp = []
			for tag in blog["tags"]:
				if "mus" not in tag and "20" not in tag and "spotify" not in tag:
					temp.append(tag)
			if "excerpt" in blog and blog["excerpt"]:
				temp.append(blog["excerpt"])
			if "short_url" in blog and blog["short_url"]:
				temp.append(blog["short_url"])
			if "summary" in blog and blog["summary"]:
				temp.append(blog["summary"])
			tumblrs[info["name"]].append(temp)

		p.append(info.copy())
		if len(p) == 3:
			repos.append(p)
			p = []
	return render_template("untitled.html", repos=repos, username=username, tumblrs=tumblrs)

app.route('/search/<name>')
def search(name):
	data = spotify.search_by_artist_name(name)
	api_url = data['playlists']['href']
	items = data['playlists']['items']
	images = data['playlists']['images']
	name = data['plylists']['name']
	html = render_template('search.html', images=images, name=name, items=items, api_url=api_url)
	return html

@app.route('/artist/<hahaha>')
def artist(hahaha):
	result = ""
	data = spotify.search_by_artist_name(hahaha)
	albums = {"total": data["albums"]["total"], "items": data["albums"]["items"], "showing": len(data["albums"]["items"])}
	tracks = {"total": data["tracks"]["total"], "items": data["tracks"]["items"], "showing": len(data["tracks"]["items"])}
	artists = {"total": data["artists"]["total"], "items": data["artists"]["items"], "showing": len(data["artists"]["items"])}
	playlists = {"total": data["playlists"]["total"], "items": data["playlists"]["items"], "showing": len(data["playlists"]["items"])}
	for i in [albums, tracks, artists, playlists]:
		for j in i["items"]:
			for k in j:
				result += str(k) + " : " + str(j[k]) + "<br><br>"
		result += "<br><br>"
	
#	return result
	return render_template("searchResult.html", albums=albums, tracks=tracks, artists=artists, playlists=playlists)




	if data["playlists"]["items"]:
		api_url = data['playlists']['href']
		items = data['playlists']['items']
		image = data['playlists']['images']
		name = data['playlists']['name']
		return render_template('searchResult.html', items=items, api_url=api_url)


if __name__ == "__main__":
	with app.app_context():
#		init_db()
		app.debug = True
		port = int(os.environ.get("PORT", 5000))
		app.run(host='0.0.0.0', port=port)
