from flask import *
from flaskext.mysql import MySQL #using pymysql/flask-mysql
import warnings

app = Flask(__name__)

# ===================== DB ===================


try:
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'p@ssw0rd'
    #app.config['MYSQL_DATABASE_DB'] = ''
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)

    conn = mysql.connect()
    cursor =conn.cursor()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cursor.execute("CREATE DATABASE IF NOT EXISTS tinta_db")
    
    #data = cursor.fetchone()
    print " > Database success"
except: print " > Database fail"


# ===================== Routing ================
@app.route('/')
def home():
	print ' > Launching home'
	return render_template("home.html")

@app.route("/about")
def about():
	print ' > Launching about'
    return render_template("about.html")


# TODO: remove
@app.route("/index2")
def index2():
    return render_template("index2.html")


if __name__ == "__main__":
    app.run(debug=True)