#!/usr/bin/python
from flask import Flask , render_template , url_for , request, jsonify
from flask import send_from_directory
# from flask_ngrok import run_with_ngrok
import sys
import os
import pandas as pd
import subprocess
from waitress import serve
from werkzeug.utils import secure_filename # this how to sanitize filename function 
from Delete_row import delete_rows_with_blank_columns 
from replaceNA import replace_na_with_blank
from texttoNum import convert_text_to_number

app = Flask(__name__,template_folder='templates' )


# make sure that uploads folder is create and configure
UPLOAD_FOLDER  = 'uploads' #hold the directory name to know that file upload could be store 
if not os.path.exists(UPLOAD_FOLDER): #if not exsite 
    os.makedirs(UPLOAD_FOLDER) #create the new folder with that name

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # This makes the path accessible from anywhere within the Flask application using app.config['UPLOAD_FOLDER'].



@app.route('/')
def waiting_web_page():
    image_url = url_for('static', filename='/picture/background/download.jpg')
    return render_template('404index.html')

@app.route('/api/deleterows', methods=['POST'])
def delete_rows():
    if  'file' not in request.files: #file presence check 
        return jsonify({"error": "No file part"}),400
    file = request.files['file'] #hold the uploaded file and information  
    if file.filename == '': # if file name not with the name and return status
        return jsonify({"error":"No selected file"}),400
    if file: # important part check secure-> 
        filename = secure_filename(file.filename)#check if the file name is secure
        #constructs the full file path where the uploaded file will be saved. It joins the configured upload directory with the sanitized filename.
        input_path = os.path.join(app.config['UPLOAD_FOLDER'],filename) 
        file.save(input_path)
        try: 
            # dont forget to create store file in function also 
            output_delrows = delete_rows_with_blank_columns(input_path)
            name, ext = os.path.splitext(filename)
            ext = ext if ext else ".xlsx"  # default to .xlsx if no extension
            output_path = save_output_file(output_delrows, f"{name}_output{ext}")
            return jsonify({
                "message": f"File processed successfully.",
                "output_path": output_path
                })
        except KeyError as e:
            return jsonify({"error": str(e)}), 400


@app.route('/api/replacevar',methods = ['POST'])
def replacevar():
    if  'file' not in request.files: #file presence check 
        return jsonify({"error": "No file part"}),400
    file = request.files['file'] #hold the uploaded file and information  
    if file.filename == '': # if file name not with the name and return status
        return jsonify({"error":"No selected file"}),400
    if file: # important part check secure-> 
        filename = secure_filename(file.filename)#check if the file name is secure
        #constructs the full file path where the uploaded file will be saved. It joins the configured upload directory with the sanitized filename.
        input_path = os.path.join(app.config['UPLOAD_FOLDER'],filename) 
        file.save(input_path)
        try: 
            # dont forget to create store file in function also 
            output_clean = replace_na_with_blank(input_path)
            name, ext = os.path.splitext(filename)
            ext = ext if ext else ".xlsx"  # default to .xlsx if no extension
            output_path = save_output_file(output_clean, f"{name}_output{ext}")
            return jsonify({
                "message": f"File processed successfully.",
                "output_path": output_path
                })
        except KeyError as e:
            return jsonify({"error": str(e)}), 400

@app.route('/api/texttonum',methods =["POST"])
def texttonum():
    if  'file' not in request.files: #file presence check 
        return jsonify({"error": "No file part"}),400
    file = request.files['file'] #hold the uploaded file and information  
    if file.filename == '': # if file name not with the name and return status
        return jsonify({"error":"No selected file"}),400
    if file: # important part check secure-> 
        filename = secure_filename(file.filename)#check if the file name is secure
        #constructs the full file path where the uploaded file will be saved. It joins the configured upload directory with the sanitized filename.
        input_path = os.path.join(app.config['UPLOAD_FOLDER'],filename) 
        file.save(input_path)
        try: 
            # dont forget to create store file in function also 
            output_clean = convert_text_to_number(input_path)
            name, ext = os.path.splitext(filename)
            ext = ext if ext else ".xlsx"  # default to .xlsx if no extension
            output_path = save_output_file(output_clean, f"{name}_output{ext}")
            return jsonify({
                "message": f"File processed successfully.",
                "output_path": output_path
                })
        except KeyError as e:
            return jsonify({"error": str(e)}), 400
    
@app.route('/output/<path:filename>')
def download_file(filename):
    return send_from_directory('output', filename, as_attachment=True)

@app.route('/main')
def index(sys=sys):
    image_url  = url_for('static', filename='/icons/terminal1.png')
    fontend = render_template('index.html')
    return render_template('index.html', image_url=image_url, fontend=fontend)
    
@app.route('/messenger')
def messenger():
    return "this is messenger page" 

def save_output_file(df, filename):
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)  # Create directory if not exists
    output_path = os.path.join(output_dir, filename)
    print(f"Saving to: {output_path}, DataFrame type: {type(df)}") 
    # Save your data (example for xlsx)
    df.to_excel(output_path, index=False)
    return output_path

mode = "prod" #dev or prod

if __name__ == "__main__":
    if mode == "dev":
        app.run(debug=True, host='localhost', port=8080)
    elif mode == "prod" :
        print("login to the webpage as http://localhost:8080")
        command = "start cmd /k ngrok http http://localhost:8080"
        subprocess.Popen(command, shell=True)
        serve(app, host='localhost', port=8080, threads=2, url_prefix="/tachdata")
    else :
        print("Unknow command")
        exit
