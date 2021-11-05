# Downloader
Descarga facil videos de plataformas como Youtube, Actualmente en fase beta y somo con youtube, proximanete Instagram y Twitter.

  ![2021-10-29-131456_276x94_scrot](https://user-images.githubusercontent.com/62490806/139483072-1f64a3f1-e39a-4062-9eab-189b3f30552c.png)
  
## Termux

Funciona en termux y descarga los videos directamente a la carpeta `/sdcard/Download`.
Descargar la Realease Android mas reciente.

## Instalación ( Python3 requerido )

### Linux / Windows / Termux

  1. Descarga la build mas reciente
  2. Entra a la carpeta que descargaste

    cd downloader
    
  3. Instala las liberias necestarias

    pip install -r requirements.txt
    
    pkg install ffmpeg  # sólo termux

  4. Inicia la aplicación
  
    python downloader.py
    
## Uso

    python downloader.py [ -D ./Directorio/ , -T (Directorio /sdcard/DCIM/Download ]

### -D

Usa -D y escribe a continuación el directorio en el que quieres que se descarguen tus archivos, por ejemplo `~/Vídeos`
     
### -T

Para termux o terminales moviles, usa el Directorio `/sdcard/DCIM/Download` asi que debes tener termux con permisos de almacenamiento


Si no escribes nada descargara en la carpeta actual.

Al ejecutar `python downloader.py` te dara la opción de elegir entre las siguientes plataformas:

### Descargar de YouTube

Pon la URL y a continuación elige si quieres descargar el video o solo el audio.

* Video: Tendras multiples opciones dependiendo de la calidad del video, las 3 primeras son las mejores si quieres descargar videos que no pesen mas de 720p, de lo contrario tendras que usar las demas opciones que descargaran por separado el audio y el video, luego seran unidos, este proceso dependera de la potencia de tu dispositivo, por lo general en Termux ira lento.
* Audio: Tendras multiples opcioens dependiendo de la calidad el audio.

### Descargar de Instagram

Pon la URL y se descargara en la carpeta que elegiste.
