from flask import Flask, flash, json,  redirect, render_template, request, url_for, make_response
from flask_bootstrap import Bootstrap4
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib, ssl
# from utils.mylogger import my_logger
# from clases.correo import email
from pymongo import database, collection, InsertOne, MongoClient


from flask_wtf.csrf import CSRFProtect

from flask_jwt_extended import create_access_token, decode_token, unset_access_cookies
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager

from forms_flask.forms import Login, Register
from config import configuracion

client = MongoClient('mongodb://localhost:27017/')
db = client['examen-luis']
collection = db['users']

app = Flask(__name__)
Bootstrap4(app)
JWTManager(app)
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html', form=Register())


@app.route('/login', methods = ['GET'])
def login():
    return render_template('login.html', form=Login())

@app.route('/register', methods=['POST'])
def registerPost():
    
    data = request.form
    port = 465 
    message = """Subject: Bienvenido a la aplicación

        Bienvenido a la aplicacion"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("Cristian.jovani2001@gmail.com", 'oeas jwyo fdhw lvui')
        server.sendmail("Cristian.jovani2001@gmail.com", data['email'], message)


    user_dict = {'username': data['username'], 'email' : data['email'], 'password': data['contrasenya']}
    collection.insert_one(user_dict)
    response = make_response(redirect(url_for('profile')))
    acceso = create_access_token(identity=json.dumps({'username': data['username']}))
    response.set_cookie(key='access_token_cookie', value=acceso)


    return response

@app.route('/profile')
@jwt_required(locations=['cookies'])
def profile():
    usuario = get_jwt_identity()
    usuario = json.loads(usuario)
    return '<h1>Bienvenido {}</h1>'.format(usuario['username'])


if __name__ == '__main__':
    app.config.from_object(configuracion['dev'])
    csrf.init_app(app)
    app.run(debug=True)
