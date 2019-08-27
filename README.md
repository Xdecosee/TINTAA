# TINTAA

Tentatively named: TINTAA; The IoT Network Traffic Analyser Application

## What it is
TINTAA is a Windows Python-based app with the intention of being able to analyse network device traffic

## Installation Requirements
Python 2 or 3

## How to run/start (windows cmd):
- Note: the virtual env is called 'virtual_env'
- Change dir to correct directory
- Install requirements by running 'pip install -r require.txt'
- Activate the virtual environment by entering: virtual_env\Scripts\activate
  - CMD should show something like: (venv) $ _
  - the virtual env has a 'local' python, any changes is made to this local venv copy
- ** Startup file changed to app.py, no longer requires setting ~~Set the startup file by entering: set FLASK_APP=main.py~~
- Run the app by entering: flask run
- View the app via http://127.0.0.1:5000/ or http://localhost:5000/
