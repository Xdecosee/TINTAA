from flask import *
from flaskext.mysql import MySQL #using pymysql/flask-mysql
import warnings
import os

# ==================== Hashing + Salting of password ====================
from passlib.hash import pbkdf2_sha256 
# param(password, iterations, saltLen default=16)
hash = pbkdf2_sha256.encrypt("password", rounds=200000, salt_size=16)
#print pbkdf2_sha256.verify("password", hash)
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


    global conn
    global cursor

    conn = mysql.connect()
    cursor =conn.cursor()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        cursor.execute("CREATE DATABASE IF NOT EXISTS tintaa_db;")
        cursor.execute("use tintaa_db")

        #username = "admin"
        #password = pbkdf2_sha256.encrypt("tintaaP@ss", rounds=200000, salt_size=16)


        cursor.execute("CREATE TABLE IF NOT EXISTS User (userID INT NOT NULL AUTO_INCREMENT, userName VARCHAR(5) NOT NULL, userPass VARCHAR(16) NOT NULL,PRIMARY KEY (userID) );")

        cursor.execute("INSERT IGNORE INTO User (userID, userName, userPass) VALUES (1, 'admin', 'tintaaP@ss');")

        #cursor.execute("CREATE TABLE IF NOT EXISTS Traffic")

        conn.commit()
    
    print " > Database success"
except: print " > Database fail"


# ===================== Routing ========================
#@app.route('/', methods=['GET', 'POST']) #Logout redirect page

@app.route('/') #Logout redirect page
def startup():
    print ' > Launching login'
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    print ' > Verifying user'

    #name = request.form['inputName']
    details = request.form
    username = details['username']
    password = details['password']
    
    cursor.execute("SELECT userPass FROM User WHERE (userName LIKE \"%s\")" % username )
    dbResult = cursor.fetchone()

    if (dbResult is None):
        print ' > Wrong username'
        return render_template("login.html")

    else:
        retrievedPwd = dbResult[0]

        if (password==retrievedPwd):
            print " > User matched"
            return render_template("devices.html")
        
        else:
            return render_template("login.html")

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

@app.route('/reset')
def reset():
    print ' > Launching reset page'
    return render_template("reset.html")

@app.route('/resetForm', methods=['POST'])
def resetForm():
    #name = request.form['inputName']
    details = request.form
    oldPwd = details['oldPwd']
    newPwd = details['newPwd']
    confirmPwd = details['confirmPwd']

    cursor.execute("SELECT userPass FROM User WHERE (userName = 'admin')" )
    dbResult = cursor.fetchone()

    retrievedPwd = dbResult[0]

    if (oldPwd==retrievedPwd):
        print " > Old password matched"

        if (newPwd == confirmPwd):
            print " > Changing password"
            cursor.execute("""UPDATE User SET userPass=%s WHERE userName = 'admin'""", ( newPwd ))
            conn.commit()
            return render_template("reset.html")
        else:
            " > New password no match"
            return render_template("reset.html")
    else:
        print " > Old password no match"
        return render_template("reset.html")


@app.route('/help')
def help():
    print ' > Launching help page'
    return render_template("help.html")


# ===================== End ========================
if __name__ == "__main__":
    app.run(debug=True)