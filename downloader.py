import json
from pytube import YouTube
import ffmpeg
from os import remove

print(""" 

===============================
=        FreeDownloads        =
=        by : Achalogy        =
=       version : 2.0.0       =
===============================

""")

def selectPlatform():
    print("""    
Selecciona la plataforma en la que quieres descargar

    1) YouTube
    0) Salir
    """)

    return input() 

def downloadFromYT(video):
    print(video.title + ' esta listo para descargar')

    ress = video.streams

    videos = [];
    audios = [];

    for x in ress:
        x1 = '{"' + str(x)[9:-1].replace(" ", ', "').replace('=', '":') + "}"
        x = json.loads(x1)
        # Simplify JSON erasing dump info

        print(x)

        if x["type"] == "video":
            # s = '{"id":"' + x["itag"] + '","type":"' + x["type"] + '","resolution":"' + x["res"] + '","fps":"' + x["fps"] + '"}'
            videos.append(x1)
        else:
            # s = '{"id":"' + x["itag"] + '","type":"' + x["type"] + '","abr":"' + x["abr"] + '"}'
            audios.append(str(x1))

    print("""
Selecciona el tipo de descarga que quieres

    1) Video
    2) Audio
    0) Salir
    """)
    t = input("")

    opts = []

    # def download(video, id):
    #     video.streams.get_by_itag(id).download()
    #     print("Video Descargado")

    def download(video, id):

        print("Descargando " + str(video.streams.get_by_itag(id).filesize / 1048576) + "MB")

        if video.streams.get_by_itag(id).includes_audio_track:
            video.streams.get_by_itag(id).download()
            print("Video Descargado")
        else:
            fvideo = video.streams.get_by_itag(id).download(filename = "video")
            videoFile = ffmpeg.input(fvideo)
            print("Video Descargado")
            faudio = video.streams.filter(only_audio=True)[0].download(filename = "audio")
            audioFile = ffmpeg.input(faudio)
            print("Audio Descargado")
            ffmpeg.output(audioFile, videoFile, (video.title + ".mp4")).run()
            print("Video Completado")
            print("Eliminando archivos basura...")
            remove(fvideo)
            remove(faudio)
            print("Archivos eliminados")

    if t == "0":
        exit()
    if t == "1":

        print("Selecciona la Calidad del Video")

        num = 0;
        for cal in videos:
            num += 1
            print(str(num) + ") " + json.loads(cal)["res"] + " " + json.loads(cal)["fps"] + " codec: " + json.loads(cal)["vcodec"])
            opts.append(json.loads(cal)["itag"])


        opt = input("")
        download(video, opts[int(opt)-1])

    elif t == "2":

        print("Seleciona la Calidad del Audio")

        num = 0;
        for cal in audios:
            num += 1
            print(str(num) + ") " + json.loads(cal)["abr"] + " codec: " + json.loads(cal)["acodec"])
            opts.append(json.loads(cal)["itag"])

        opt = input("")

        download(video, opts[int(opt)-1])

    else:
        print('Selecciona una opcion valida')



s = selectPlatform()

if s == "0":
    exit()
elif s == "1": 
    # try:
        video = YouTube(input('url: '))
        downloadFromYT(video)
    # except:
        # print('Por Favor usa una url valida')
else:
    print('Elige una opcion')



