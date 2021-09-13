import base64
import os

from flask_cors import CORS
from flask import Flask, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER_IMAGES = './static/images'
UPLOAD_FOLDER_DOCUMENTOS = './static/documentos'
app = Flask(__name__)
app.config['UPLOAD_FOLDER_IMAGES'] = UPLOAD_FOLDER_IMAGES
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods = ['GET', 'POST'])
def upload_arquivos():
    iddb = request.args.get('db')
    iduser = request.args.get('iduser')

    #verifica se tem arquivo na requisição
    if 'file' not in request.files:
        return 'Não há arquivo'
    #verifica se a pasta do db existe, se não existir cria uma
    if not os.path.isdir(app.config['UPLOAD_FOLDER_IMAGES']+f'/{iddb}'):
        os.mkdir(app.config['UPLOAD_FOLDER_IMAGES']+f'/{iddb}')

    file = request.files['file']
    filename = secure_filename(file.filename)
    extension = filename.split('.')
    name_file = f'img_{iddb}_{iduser}.{extension[len(extension) -1]}'
    file.save(os.path.join(app.config['UPLOAD_FOLDER_IMAGES']+f'/{iddb}',name_file))
    return f'/{iddb}/{name_file}'

@app.route('/rename', methods=['GET'])
def rename_file():
    oldname = request.args.get('oldname')
    newName = request.args.get('newname')
    basepath = request.args.get('base')
    extension = oldname.split('.')
    old_file = os.path.join(app.config['UPLOAD_FOLDER_IMAGES']+f'/{basepath}',oldname)
    new_file = os.path.join(app.config['UPLOAD_FOLDER_IMAGES']+f'/{basepath}',f'{newName}.{extension[1]}')
    os.rename(old_file,new_file)
    return f'/{basepath}/{newName}.{extension[1]}'

@app.route('/createimg', methods=['POST'])
def createimg():
    iddb = request.args.get('db')
    iduser = request.args.get('iduser')
    obj = request.get_json()
    ia = obj.get('img').split(',')


    if not os.path.isdir(app.config['UPLOAD_FOLDER_IMAGES']+f'/{iddb}'):
        os.mkdir(app.config['UPLOAD_FOLDER_IMAGES']+f'/{iddb}')
    aux = ia[0].split('/')
    extensao = aux[1].split(';')
    filename = f'img_{iddb}_{iduser}.{extensao[0]}'
    with open(app.config['UPLOAD_FOLDER_IMAGES']+f'/{iddb}/{filename}','wb') as novaimagem:
        novaimagem.write(base64.b64decode(ia[1]))

    return f'/{iddb}/{filename}'

if __name__ == '__main__':
    app.run()
