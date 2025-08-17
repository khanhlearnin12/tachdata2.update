#!/usr/bin/python
from flask import Flask , render_template , url_for
# from flask_ngrok import run_with_ngrok
import main
import sys

app = Flask(__name__,template_folder='templates' )
# run_with_ngrok(app)

@app.route('/')
def waiting_web_page():
    image_url = url_for('static', filename='/picture/background/download.jpg')
    return render_template('404index.html')

@app.route('/chosingpath', methods=['POST'])
def chosingpath(sys=sys):    
    return "Hello, friends"

@app.route('/main')
def index(sys=sys):
    image_url  = url_for('static', filename='/picture/icons/terminal.png')
    fontend = render_template('index.html')
    return render_template('index.html', image_url=image_url, fontend=fontend)

@app.route('/messenger')
def messenger():
    return "this is messenger page" 

# @app.route('/delete_rows', methods=["POST"])
# def delete_rows_with_blank_columns():
#     excel_file_path = ''
#     output_file_path = ''
#     main.delete_rows_with_blank_columns(excel_file_path, output_file_path)

if __name__ == "__main__":
    # app.run()
    app.run(debug=True, host='localhost', port=5000)

