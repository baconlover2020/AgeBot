import painel
import requests
from bs4 import BeautifulSoup

def generate_mp3(youtube_url, nome_arquivo):
    url = 'https://www.easymp3converter.com/models/convertProcess.php'
    payload = { 'type': 'mp3',
                'search_txt': youtube_url
                }
    r = requests.post(url, data=payload)
    soup = BeautifulSoup(r.content,'html.parser')
    link = soup.find_all('option')[-1].get('data-link')
    duration = soup.find(class_='video_duration').string
    minutos, segundos = duration.split(':')
    length = int(minutos) * 60 + int(segundos)
    song_data = '1:'+nome_arquivo.split('_')[-1]+','+str(length)
    return  download_mp3(link, nome_arquivo), song_data, nome_arquivo
    
        

def download_mp3(link, nome_arquivo):
    r = requests.get(link, stream=True, verify=False)
    path = f"musicas/{nome_arquivo}.mp3"
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=None):
            f.write(chunk)
    return path

def get_file_number():
    with open('musicas/music_ids.txt', 'r') as f:
        file_number = int(f.readline()) + 1
        song_id = f.readline()
        furni_id = f.readline()
    with open('musicas/music_ids.txt', 'w+') as f:
        f.writelines(str(file_number)+'\n')
        f.writelines(song_id)
        f.writelines(furni_id)
    return str(file_number)

def get_song_id():
    with open('musicas/music_ids.txt', 'r') as f:
        file_number = f.readline()
        song_id = int(f.readline()) + 1
        furni_id = f.readline()
    with open('musicas/music_ids.txt', 'w+') as f:
        f.writelines(file_number)
        f.writelines(str(song_id)+'\n')
        f.writelines(furni_id)
    return str(song_id)

def get_furni_id():
    with open('musicas/music_ids.txt', 'r') as f:
        file_number = f.readline()
        song_id = f.readline()
        furni_id = int(f.readline()) + 1
    with open('musicas/music_ids.txt', 'w+') as f:
        f.writelines(file_number)
        f.writelines(song_id)
        f.writelines(str(furni_id)+'\n')
    return str(furni_id)


nome_musica = input('Digite o nome da musica')
artista = input('Digite o nome do artista')
youtube_url = input('Digite o link do youtube')
mp3, song_data, nome_arquivo = generate_mp3(youtube_url, 'sound_machine_sample_' + get_file_number().replace('\n', ''))
painel.login()
painel.adicionar_musica(mp3, song_data, nome_arquivo, nome_musica, artista, get_song_id(), get_furni_id())

