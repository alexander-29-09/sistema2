from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
import os
from flask_bootstrap import Bootstrap
from threading import Thread

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

def limpiar_nombre(nombre):
    caracteres_invalidos = '\\/:*?"<>|'
    for caracter in caracteres_invalidos:
        nombre = nombre.replace(caracter, '_')
    return nombre

def descargar_video(url, formato):
    try:
        video = YouTube(url)
        if formato == 'video':
            stream = video.streams.get_highest_resolution()
            extension = "mp4"    
        else:
            stream = video.streams.filter(only_audio=True).first()
            extension = "mp3"

        carpeta_descargas = os.path.expanduser('~\Downloads')
        nombre_archivo = limpiar_nombre(video.title)
        nombre_archivo += f".{extension}"
        
        stream.download(output_path=carpeta_descargas, filename=nombre_archivo)
        return f"Descarga completada en la carpeta de Descargas. Nombre del archivo: {nombre_archivo}"

    except Exception as e:
        return f"Ocurrió un error al descargar el archivo. Error: {str(e)}"

@app.route('/descargar', methods=['POST'])
def descargar_handler():
    url = request.form['url']
    formato = request.form['formato']

    def descargar_video_thread():
        estado = descargar_video(url, formato)
        with app.app_context():
            app.estado_descarga = estado

    descarga_thread = Thread(target=descargar_video_thread)
    descarga_thread.start()

    return render_template('index.html', estado_descarga=app.estado_descarga)
#descarga video
@app.route('/descargas')
def ver_descargas():
    carpeta_descargas = os.path.expanduser('~\Downloads')
    return send_from_directory(carpeta_descargas, as_attachment=True)

if __name__ == '__main__':
    app.estado_descarga = None
    app.run(debug=True)
