#!/usr/bin/python
from flask import Flask , render_template 
# from flask_ngrok import run_with_ngrok
import main
import sys

app = Flask(__name__,template_folder='templates' )
# run_with_ngrok(app)

@app.route('/')
def waiting_web_page():
    return render_template('waiting-web-page/404index.html')

@app.route('/chosingpath', methods=['POST'])
def chosingpath():
    return "Hello, friends"

@app.route('/main')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # app.run()
    app.run(debug=True, host='localhost', port=5000)