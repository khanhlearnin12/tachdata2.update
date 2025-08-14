#!/usr/bin/python
from flask import Flask , render_template 
# from flask_ngrok import run_with_ngrok
import main
import sys

app = Flask(__name__,template_folder='templates', waiting_web_page ='waiting-web-page')
# run_with_ngrok(app)

@app.route('/waiting')
def waiting_web_page():
    return render_template('waiting-web-page/index.html')

@app.route('/chosingpath')
def chosingpath():
    return "Hello, friends"

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # app.run()
    app.run(debug=True, host='localhost', port=5000)