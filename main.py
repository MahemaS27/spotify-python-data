# Import libraries
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# get username from terminal

username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# erase cache and ask user for perms

try:
  token = util.prompt_for_user_token(username,scope)
except (AttributeError,JSONDecodeError):
  os.remove(f".cache-{username}")
  token = util.prompt_for_user_token(username, scope)


# above will open a web page to ask for permssions to use spotify account
# will also remove old data every launch from terminal

# create spotify object

spotifyObject = spotipy.Spotify(auth=token)

# display which device we're playing from

devices = spotifyObject.devices()
print(json.dumps(devices, sort_keys=True,indent=4))
deviceId = devices['devices'][0]["id"]

# Get the track info
track = spotifyObject.current_user_playing_track()
print(json.dumps(track, sort_keys=True, indent=4))
print()
artist = track["item"]["artists"][0]["name"]
track = track["item"]['name']

if artist !="":
  print("Currently playing " + artist + " - " + track)

# user information

user = spotifyObject.current_user()
displayName = user['display_name']
followers = user['followers']['total']


# this is what will be running during the application

while True:
  print()
  print("Wecome to Spotify,"+ displayName + " :")
  print(">>> Welcome to Spotify " + displayName + " :)")
  print(">>> You have " + str(followers) + " followers.")
  print()
  print("0 - Search for an artist")
  print("1 - exit")
  print()
  choice = input("Enter your choice: ")

  # search for artist choice
  if choice == "0":
    print()
    searchQuery = input("What is the artist's name?: ")
    print()

    # get search results

    results = spotifyObject.search(searchQuery,1,0,"artist")

    #print artist details
    artist = results['artists']['items'][0]
    print(artist['name'])
    print(str(artist['followers']['total']) + " followers")
    print(artist['genres'][0])
    print()
    webbrowser.open(artist['images'][0]['url'])
    artistID = artist['id']

    # Album details
    trackURIs = []
    trackArt = []
    z = 0

    # Extract data from album
    albumResults = spotifyObject.artist_albums(artistID)
    albumResults = albumResults['items']

    for item in albumResults:
      print("ALBUM: " + item['name'])
      albumID = item['id']
      albumArt = item['images'][0]['url']

      # Extract track data
      trackResults = spotifyObject.album_tracks(albumID)
      trackResults = trackResults['items']

      for item in trackResults:
        print(str(z) + ": " + item['name'])
        trackURIs.append(item['uri'])
        trackArt.append(albumArt)
        z+=1
      print()


    # See album art
    while True:
      songSelection = input("Enter a song number to see the album art (or press x to exit): ")
      if songSelection == "x":
        break
      trackSelectionList = []
      trackSelectionList.append(trackURIs[int(songSelection)])
      spotifyObject.start_playback(deviceId, None, trackSelectionList)
      webbrowser.open(trackArt[int(songSelection)])

  if choice == 1:
    # end the program
    break