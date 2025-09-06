#!/usr/bin/python
from flask import Flask , render_template , url_for , request, jsonify
# from flask_ngrok import run_with_ngrok
import sys
import os
from werkzeug.utils import secure_filename #what is this ?? 
from  Delete_row import delete_rows_with_blank_columns 
app = Flask(__name__,template_folder='templates' )


# what is this part do ??
UPLOAD_FOLDER  = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def waiting_web_page():
    image_url = url_for('static', filename='/picture/background/download.jpg')
    return render_template('404index.html')

@app.route('/api/deleterows', methods=['POST'])
def delete_rows():
    if  'file' not in request.files:
        return jsonify({"error": "No file part"}),400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error":"No selected file"}),400
    if file:
        filename = secure_filename (file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(input_path)
        try: 
            output_path = delete_rows_with_blank_columns(input_path)
            return jsonify({"message": f"File processed successfully. Cleaned file saved at {output_path}"})
        except KeyError as e:
            return jsonify({"error": str(e)}), 400


@app.route('/main')
def index(sys=sys):
    image_url  = url_for('static', filename='/icons/terminal1.png')
    fontend = render_template('index.html')
    return render_template('index.html', image_url=image_url, fontend=fontend)
    
@app.route('/messenger')
def messenger():
    return "this is messenger page" 


if __name__ == "__main__":
    # app.run()
    app.run(debug=True, host='localhost', port=5000)

