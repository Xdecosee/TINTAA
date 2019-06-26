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
@app.route('/') #Logout redirect page
def home():
	print ' > Launching home'
	return render_template("home.html")

@app.route('/login') 
def login():
	print ' > Launching login'
	return render_template("login.html")

@app.route('/signup') 
def signup():
	print ' > Launching signup'
	return render_template("signup.html")

@app.route('/devices')
def devices():
    print ' > Launching devices'
    return render_template("devices.html")

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


if __name__ == "__main__":
    app.run(debug=True)