from flask import *
import identify
import capturetraffic
from flaskext.mysql import MySQL #using pymysql/flask-mysql
import warnings
import os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/') #Logout redirect page
def startup():
    print(' > Launching startup')
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    return render_template("start.html")


@app.route('/start')
def start():
    print(' > Launching start')
    return render_template("start.html")


@app.route('/devices')
def devices():
    print('Getting Live Devices...')
    input = "192.168.1.0/24"
    #input = "192.168.4.1/24"
    #Scan for Live Hosts 
    dev_list = identify.scan_devices(input)
    Ip = []
    Mac = []
    Vendor = []
    for dev in dev_list :
        Ip.append(dev[0])
        Mac.append(dev[1])
        Vendor.append(dev[2])

    return render_template("devices.html", len = len(dev_list), Ip = Ip, Mac = Mac , Vendor = Vendor)
    
@app.route('/capture')
def capture():
    print('Starting Capture.... (Up to 10 Packets)')
    packetlist = capturetraffic.startcapture()
    Src = []
    Dst = []
    Packet = []
    for p in packetlist:
        Src.append(p[0])
        Dst.append(p[1])
        Packet.append(p[2])

    return render_template("capture.html" , len = len(packetlist), Src = Src, Dst = Dst , Packet = Packet)

@app.route('/deviceDetails')
def deviceDetails():
    print(' > Launching devices details')
    return render_template("deviceDetails.html")




@app.route('/update', methods=['POST'])
def update():
    print(' > Updating device name')

    details = request.form
    newName = details['deviceName']
    
    cursor.execute("SELECT deviceName FROM Traffic WHERE (deviceName LIKE \"%s\")" % newName )
    dbResult = cursor.fetchall()

    #oldName = temp TODO
    
    cursor.execute("""UPDATE Traffic SET deviceName=%s WHERE deviceName = %s""", ( newName, oldName ))
    conn.commit()






@app.route('/reset')
def reset():
    print(' > Launching reset page')
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
        print(" > Old password matched")

        if (newPwd == confirmPwd):
            print(" > Changing password")
            cursor.execute("""UPDATE User SET userPass=%s WHERE userName = 'admin'""", ( newPwd ))
            conn.commit()
            return render_template("reset.html")
        else:
            " > New password no match"
            return render_template("reset.html")
    else:
        print(" > Old password no match")
        return render_template("reset.html")


@app.route('/help')
def help():
    print(' > Launching help page')
    return render_template("help.html")


# ===================== End ========================
if __name__ == "__main__":
    app.run(debug=True)
    