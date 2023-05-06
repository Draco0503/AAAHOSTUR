import os
from dotenv import load_dotenv
from flask import Flask, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# CONFIG FOR CUSTOM OAUTH SERVER
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')
app.config['DEBUG'] = os.getenv('DEBUG')

# CONFIG FOR MYSQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
mysql = MySQL(app)


@app.route('/')
def index():
    return '<h1>Hello world</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)