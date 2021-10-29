import os
from pytube import YouTube
import instaloader
from instaloader import Post
import ffmpeg
import json
import shutil
import sys 

print(""" 

===============================
=        FreeDownloads        =
=        by : Achalogy        =
=       version : 3.0.1       =
===============================

""")

def selectPlatform():
    print("""    
Selecciona la plataforma en la que quieres descargar

     1) YouTube
     2) Instagram
     0) Salir
    """)

    return input() 

def downloadFromYT(video, downloadDir):
    print(video.title + ' esta listo para descargar')

    ress = video.streams

    videos = [];
    audios = [];

    for x in ress:
        x1 = '{"' + str(x)[9:-1].replace(" ", ', "').replace('=', '":') + "}"
        x = json.loads(x1)
        if x["type"] == "video":
            videos.append(x1)
        else:
            audios.append(str(x1))

    print("""
Selecciona el tipo de descarga que quieres

     1) Video
     2) Audio
     0) Salir
    """)
    t = input("")

    opts = []
    optsAud = []

    def download(video, id, aud):


        if video.streams.get_by_itag(id).includes_audio_track:
            print("Descargando " + str(round(video.streams.get_by_itag(id).filesize_approx / 1048576, 1)) + "MB")
            fileD = video.streams.get_by_itag(id).download() 
            shutil.move(fileD, downloadDir)
            print("Video Descargado")
        else:
            fvideo = video.streams.get_by_itag(id)

            if aud == 0:
                faudio = video.streams.filter(only_audio=True).last()
            else:
                faudio = video.streams.get_by_itag(aud)

            file_video = fvideo.download(filename = "video")
            file_audio = faudio.download(filename = "audio")

            print("Descargando " + str(round((fvideo.filesize_approx / 1048576) + (faudio.filesize_approx / 1048576), 1)) + "MB")

            videoFile = ffmpeg.input(file_video)
            print("Video Descargado")
            audioFile = ffmpeg.input(file_audio)
            print("Audio Descargado")
            fileD = ffmpeg.output(audioFile, videoFile, ("./" + video.title + ".mp4")).run() # Mismo directorio
            print("Video Completado")
            print("Eliminando archivos basura...")
            os.remove(file_video)
            os.remove(file_audio)
            print("Archivos eliminados")

            shutil.move("./" + video.title + ".mp4", downloadDir)

    if t == "0":
        exit()
    if t == "1":

        print("Selecciona la Calidad del Video")

        num = 0;
        for cal in videos:
            num += 1

            fileSizeApprox = 0;

            if num == 1:
                print("Video con audio")
            elif num == 4:
                print("Audio Separado")

            if num >= 1 < 4:
                fileSizeApprox += video.streams.get_by_itag(json.loads(cal)["itag"]).filesize_approx / 1048576
            if num >= 4:
                fileSizeApprox += (video.streams.get_by_itag(json.loads(cal)["itag"]).filesize_approx / 1048576) + (video.streams.filter(only_audio=True).last().filesize_approx / 1048576)

            print("     " + str(num) + ") " + json.loads(cal)["res"] + " " + json.loads(cal)["fps"] + " codec: " + json.loads(cal)["vcodec"] + "  - Filesize approx = " + str(round(fileSizeApprox, 1)) + "Mb")
            opts.append(json.loads(cal)["itag"])


        opt = input("")

        if int(opt) > 3:

            HD = video.streams.filter(only_audio=True).last()

            print("Ahora selecciona el archivo de Audio a descargar")
            print("     0) Mayor calidad: " + str(round(HD.filesize_approx / 1048576, 1)) + "Mb")

            num = 0
            for cal in audios:
                num += 1

                fileSizeApprox = video.streams.get_by_itag(json.loads(cal)["itag"]).filesize_approx / 1048576;

                print("     " + str(num) + ") " + json.loads(cal)["abr"] + " codec: " + json.loads(cal)["acodec"] + "  - Filesize approx = " + str(round(fileSizeApprox, 1)) + "Mb")
                optsAud.append(json.loads(cal)["itag"])

            optAUD = int(input(""))

            if optAUD == 0:
                 download(video, opts[int(opt)-1], 0)
            else:
                download(video, opts[int(opt)-1], optsAud[int(optAUD)-1])

        else:
            download(video, opts[int(opt)-1], opts[int(opt)-1])

    elif t == "2":

        print("Seleciona la Calidad del Audio")

        num = 0;
        for cal in audios:
            num += 1

            fileSizeApprox = video.streams.get_by_itag(json.loads(cal)["itag"]).filesize_approx / 1048576;

            print("     " + str(num) + ") " + json.loads(cal)["abr"] + " codec: " + json.loads(cal)["acodec"] + "  - Filesize approx = " + str(round(fileSizeApprox, 1)) + "Mb")
            opts.append(json.loads(cal)["itag"])

        opt = input("")

        download(video, opts[int(opt)-1])

    else:
        print('Selecciona una opcion valida')

def downloadFromIg(post, insta, downloadDir):
    insta.download_post(post, target="InstagramTemp")
    files = os.listdir("./InstagramTemp")

    for item in files:
        if item.endswith(".json.xz") | item.endswith(".txt"): 
            os.remove(os.path.join("./InstagramTemp/" + item))
        else:
            shutil.move("./InstagramTemp/" + item, downloadDir)


downloadDir = "./"

if len(sys.argv) > 1:
    if sys.argv[1] == "-D":
        print('case 1')
        downloadDir = sys.argv[2]

        if not downloadDir.endswith("/"):
            downloadDir = str(sys.argv[2] + "/")

    elif sys.argv[1] == "-T":
        downloadDir = "/sdcard/DCIM/Download"
    
    else:
        downloadDir = downloadDir

s = selectPlatform()

print("Dirección de Descarga: " + downloadDir)

if s == "0":
    exit()
elif s == "1": 
    try:
        video = YouTube(input('url: '))
        downloadFromYT(video, downloadDir)
    except:
        print('Algo salio mal, asegurate que usaste una URL valida.')
elif s == "2":

    insta = instaloader.Instaloader()

    try:
        post = Post.from_shortcode(insta.context, (input("URL:")[28:])[:11])
        downloadFromIg(post, insta, downloadDir)
    except:
        print('Algo salio mal, asegurate que usaste una URL valida.')

else:
    print('Elige una opcion')