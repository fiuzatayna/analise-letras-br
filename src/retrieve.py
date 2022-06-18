import json
import requests
import pandas as pd

import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from PIL import Image

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
def pega_musica(artista=None, titulo=None, chave=None):
    
    print("Buscando música \""+titulo+"\" de "+artista+"...")
    
    try:
        response = requests.get("https://api.vagalume.com.br/search.php?art="+artista+"&mus="+titulo+"&extra=alb&apikey={"+chave+"}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
        
    return response

def songs_to_dataframe(song_dict=None, chave=None):
    
    idiomas = {
    1:"Português (BR)",
    2:"Inglês",
    3:"Espanhol",
    4:"Francês",
    5:"Alemão",
    6:"Italiano",
    7:"Holandês",
    8:"Japonês",
    9:"Português (PT)",
    999999:"Outros"
    }
    
    #O Vagalume tem um sistema de números para indicar os idiomas, [confira aqui](https://api.vagalume.com.br/docs/letras/).

    song_df = pd.DataFrame(columns=['artista', 'id_artista', 'url_artista',
                                    'titulo', 'letra', 'idioma', 'url', 'id_musica',
                                   'album', 'id_album', 'url_album', 'capa_album', 'ano_album'])

    for song in song_dict:

        titulo = song
        artista = song_dict[song]

        response = pega_musica(artista=artista, titulo=titulo, chave=chave)

        artist_info = response.json()['art']
        artista = artist_info['name']
        id_artista = artist_info['id']
        url_artista = artist_info['url']

        song_info = response.json()['mus'][0]
        titulo = song_info['name']
        letra = song_info['text']
        url = song_info['url']
        id_musica = song_info['id']
        idioma =  idiomas[song_info['lang']]

        album_info = song_info['alb']
        album = album_info['name']
        id_album = album_info['id']
        url_album = album_info['url']
        capa_album = album_info['img']
        ano_album = album_info['year']

        esta_musica = pd.DataFrame([[artista, id_artista, url_artista,
                                     titulo, letra, idioma, url, id_musica,
                                    album, id_album, url_album, capa_album, ano_album]], 
                                   columns=['artista', 'id_artista', 'url_artista',
                                            'titulo', 'letra', 'idioma', 'url', 'id_musica',
                                           'album', 'id_album', 'url_album', 'capa_album', 'ano_album'])
        song_df = pd.concat([song_df, esta_musica])

    song_df.reset_index(inplace=True, drop=True)
    return song_df

def testa_link(link):
    print(link)
    req = Request(link)
    try:
        response = urlopen(link)
    except HTTPError as e:
        # do something
        print('Código do Erro: ', e.code)
    except URLError as e:
        # do something
        print('Motivo: ', e.reason)
    else:
        # do something
        print('O link funciona!') 
        
def baixa_capa(url_capa, output_file):
    output_path = '../images/'+output_file+'.webp'
    urllib.request.urlretrieve(url_capa, output_path)
    return output_path

def aumenta_imagem(input_file):
    image = Image.open(input_file)
    new_image = image.resize((1500, 1500))
    new_name = '.'.join(input_file.split('.')[:-1])+'_big.'+''.join(input_file.split('.')[-1])
    new_image.save(new_name)
    
    return new_name
    