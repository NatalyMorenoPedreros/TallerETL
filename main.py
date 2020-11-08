import spotipy
import psycopg2 as pg


sp = spotipy.Spotify()

from spotipy.oauth2 import SpotifyClientCredentials

cid = "98e6ac0f94a346f2b05931f2931e9dd8"
secret = "fa9b0c4736c7444db761ffff2a402537"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

playlist = sp.user_playlist("2j61gdsxsbasor816f1dnbpk3", "spotify:playlist:4NCX2yraYQKMCX6X8NQRfm", fields="tracks")
tracks = playlist["tracks"]
songs = tracks["items"]

ids = []
song = []
artist = []

connection = pg.connect(user='nataly',password='1234',host='localhost',database='MUSICA',port='5432')
cursor = connection.cursor()


def validate(idartists,idartist):
    for i in range(len(idartists)):
        if idartists[i] == idartist:
            return True
    return False


for i in range(len(songs)):
    s = songs[i]["track"]
    query_track = "INSERT INTO tracks(nombre,tipo,artista,album,numero,popularidad,idspotify,uri,fechalanzamiento,fechacarga,origen) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    record_query_t = (s["name"],s["type"],s["artists"][0]["name"],s["album"]["name"],s["track_number"],
                    s["popularity"],s["id"],s["uri"],s["album"]["release_date"],'NOW()',s['external_urls']['spotify'])

    cursor.execute(query_track, record_query_t)
    query_artist = "INSERT INTO artist(nombre,popularidad,tipo,uri,cantidadseguidores,fechacarga,origen) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    a = sp.artist(s["artists"][0]["id"])
    id_artist = a["id"]
    if not validate(ids,id_artist):
        ids.append(a["id"])
        record_query_a = (a["name"], a["popularity"],a["type"],a["uri"],a["followers"]["total"],'NOW()',a['external_urls']['spotify'])
        cursor.execute(query_artist, record_query_a)
        connection.commit()

connection.close()
print("Proceso terminado...:)")
