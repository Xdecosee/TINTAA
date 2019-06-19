from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def home():
	print ' ** running'
	return render_template("home.html")
	
	
@app.route("/page2")
def page2():
    return "Hello, page2"

if __name__ == "__main__":
    app.run(debug=True)