from flask import Flask, render_template, request, send_file, send_from_directory
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)

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

        nombre_archivo = limpiar_nombre(video.title)
        nombre_archivo += f".{extension}"

        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, nombre_archivo)
        stream.download(output_path=temp_dir, filename=nombre_archivo)
        
        return file_path

    except Exception as e:
        return None, f"Ocurrió un error al descargar el archivo. Error: {str(e)}"

@app.route('/descargar', methods=['POST'])
def descargar_handler():
    url = request.form['url']
    formato = request.form['formato']

    file_path = descargar_video(url, formato)
    if file_path:
        return send_file(file_path, as_attachment=True)
    else:
        return render_template('index.html', estado_descarga="Ocurrió un error al descargar el archivo.")

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('templates', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
