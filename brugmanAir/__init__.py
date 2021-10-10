from flask import Flask
from itertools import zip_longest
from flask_mysqldb import MySQL



app = Flask(__name__)

# config MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "06840564M#2"
app.config["MYSQL_DB"] = "brugmanair"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "secret123"

# init MYSQL
mysql = MySQL(app)

from brugmanAir.flight import routes
from brugmanAir.beheerder import routes
