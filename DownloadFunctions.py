from __future__ import unicode_literals
import youtube_dl, mutagen, os, re, requests, sys
import urllib, ssl, glob
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON
from mutagen.mp3 import MP3
from PIL import Image
from io import BytesIO
"""
Torin Foss | tfoss@csumb.edu | 2018
"""

def get_soup(url):
    """
    Returns a BeautifulSoup object.
    """
    context = ssl._create_unverified_context()
    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    resp = urlopen(req, context=context)
    soup = BeautifulSoup(resp.read(), 'lxml')
    return soup

def get_url(search):
    """
    Returns a url as a string to be used by our
    youtube-dl object.
    Scrapes youtube for a video that has
    track and artist in the name.
    """
    query = urllib.parse.quote(search)
    url = "https://www.youtube.com/results?search_query=" + query
    soup = get_soup(url)
    search_results = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        search_results.append('https://www.youtube.com' + vid['href'])
    return search_results[1]

def get_ydl_obj():
    """
    Returns a youtube-dl object with
    the specified parameters.
    """
    ydl_opts = {
                'format': 'bestaudio/best', # get best audio
                'outtmpl': 'YDL/%(id)s.%(ext)s', # sets output template
                'nocheckcertificate': True, # bypasses certificate check
                'noplaylist' : True, # won't download playlists
                # 'quiet': True, #suppress messages in command line
                'postprocessors':
                    [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }]
                }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    return ydl

def download(queryDict):
    """
    Downloads songs from youtube.
    """
    # for song in queries:
    ydl = get_ydl_obj()
    url = get_url(queryDict['title'] + " " + queryDict['artist'])
    ydl.download([url])
    path = glob.glob("YDL/*.mp3")[0]
    set_data(path, queryDict)
    # set_cover_art(path, queryDict)
    set_file_path(path, queryDict)



def set_data(path, song):
    """
    Sets the ID3 meta data of the MP3 file
    found at the end of path.

    Song must be a dict
    """
    new_song = ID3(path)
    new_song.delete()
    new_song.add(TIT2(encoding=3, text=song['title']))
    new_song.add(TPE1(encoding=3, text=song['artist']))
    new_song.add(TALB(encoding=3, text=song['album']))
    # new_song.add(TCON(encoding=3, text=song.primary_genre_name))
    new_song.save()
    return

def set_cover_art(path, song):
    """
    Embeds a jpg file into the ID3 meta data
    of the mp3 file found at the end of path.

    Song must be a track object
    """
    mutagen_song = MP3(path, ID3=ID3)
    img_url = song.artwork_url_100
    img_save_id = "CoverArt/"+song.collection_name+".jpg"
    img_response = requests.get(img_url)
    img = Image.open(BytesIO(img_response.content))
    img.save(img_save_id)
    mutagen_song.tags.add(APIC(encoding=3, mime="image/jpg",
                           type=3, desc=u"Cover",
                           data=open(img_save_id, "rb").read()))
    mutagen_song.save()
    return

def set_file_path(path, song):
    """
    Sets the file path of song to:
    YDL/[artist]/[album]/[track].mp3
    In order to easily be found.
    """
    if sys.platform == "win32":
        mv_dir_windows(path, song)
    else:
        mv_dir_mac(path, song)

def mv_dir_windows(path, song):
    """
    Commands for creating directories,
    and moving files for windows.
    """
    new_dir = '"' + 'Fixed/'+song.artist_name+ '/'+ song.collection_name+ '/' +'"'
    os.system("mkdir %s" % (new_dir.replace(" ", "_")))

    new_path = "Fixed/"+song.artist_name+ "/"+ song.collection_name+ "/"+song.track_name+".mp3"
    new_path = '"'+new_path+'"'
    old_path = '"'+path+'"'
    os.system("move %s %s" % (old_path, new_path.replace(" ", "_")))
    return


def mv_dir_mac(path, song):
    """
    Commands for creating directories,
    and moving files for windows.
    """
    # make dir with artist name
    new_dir = '"' + 'Fixed/'+song['artist']+ '/' + '"'
    os.system("mkdir -p %s" % (new_dir.replace(" ", "_")))
    # make dir with album name
    new_dir = '"' + 'Fixed/'+song['artist']+ '/'+ song['album']+ '/' +'"'
    os.system("mkdir -p %s" % (new_dir.replace(" ", "_")))
    # add song to album dir
    new_path = "Fixed/"+song['artist']+ "/"+ song['album']+ "/"+song['title']+".mp3"
    new_path = '"'+new_path+'"'
    old_path = '"'+path+'"'
    os.system("mv %s %s" % (old_path, new_path.replace(" ", "_")))
    return

"""
MAIN
"""
# test = {
#     'title':'future development', 
#     'artist':'del the funkee homosapien',
#     'album':'future development'
# }
# download(test)