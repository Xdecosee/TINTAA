from flask import *
from flaskext.mysql import MySQL #using pymysql/flask-mysql
import warnings
import os

# ==================== Hashing + Salting of password ====================
from passlib.hash import pbkdf2_sha256 
# param(password, iterations, saltLen default=16)
hash = pbkdf2_sha256.encrypt("password", rounds=200000, salt_size=16)
print pbkdf2_sha256.verify("password", hash)
# ==================== End ====================

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

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


# ===================== Routing ========================
@app.route('/') #Logout redirect page
def home():
	print ' > Launching home'
	return render_template("home.html")

@app.route('/login') 
def login():
	print ' > Launching login'
	return render_template("login.html")

@app.route('/register') 
def register():
	print ' > Launching register'
	return render_template("register.html")

@app.route('/devices')
def devices():
    print ' > Launching devices'
    return render_template("devices.html")

@app.route('/start')
def start():
    print ' > Launching start'
    return render_template("start.html")

@app.route('/deviceDetails')
def deviceDetails():
    print ' > Launching devices details'
    return render_template("deviceDetails.html")

@app.route('/archive')
def archive():
    print ' > Launching archive'
    return render_template("archive.html")

@app.route('/reset')
def reset():
    print ' > Launching reset page'
    return render_template("reset.html")

@app.route('/help')
def help():
    print ' > Launching help page'
    return render_template("help.html")


# ===================== End ========================
if __name__ == "__main__":
    app.run(debug=True)