import json
from pytube import YouTube
import ffmpeg
from os import remove

print(""" 

===============================
=        FreeDownloads        =
=        by : Achalogy        =
=       version : 2.1.0       =
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
    optsAud = []

    # def download(video, id):
    #     video.streams.get_by_itag(id).download()
    #     print("Video Descargado")

    def download(video, id, aud):


        if video.streams.get_by_itag(id).includes_audio_track:
            print("Descargando " + str(round(video.streams.get_by_itag(id).filesize_approx / 1048576, 1)) + "MB")
            video.streams.get_by_itag(id).download() # Mismo directorio
            # video.streams.get_by_itag(id).download(output_path = "/sdcard/Download") # Directorio Descargas ( Termux )
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
            ffmpeg.output(audioFile, videoFile, (video.title + ".mp4")).run() # Mismo directorio
            # ffmpeg.output(audioFile, videoFile, ("/sdcard/Download/" + video.title + ".mp4")).run() # Directorio Descargas ( Termux )
            print("Video Completado")
            print("Eliminando archivos basura...")
            remove(file_video)
            remove(file_audio)
            print("Archivos eliminados")

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



