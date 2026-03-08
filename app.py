from flask import Flask , render_template , url_for , request, jsonify
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
# from flask_ngrok import run_with_ngrok
import sys
import os
import pandas as pd
import subprocess
from waitress import serve
from werkzeug.utils import secure_filename # this how to sanitize filename function 
from werkzeug.security import generate_password_hash 
from Delete_row import delete_rows_with_blank_columns 
from replaceNA import replace_na_with_blank
from texttoNum import convert_text_to_number

#create app on flash
app = Flask(__name__,template_folder='templates')
# connect to the database 
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Định nghĩa bảng User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) # Lưu hash, không lưu plain text!
    email = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():
    db.create_all()



# make sure that uploads folder is create and configure
UPLOAD_FOLDER  = 'uploads' #hold the directory name to know that file upload could be store 
if not os.path.exists(UPLOAD_FOLDER): #if not exsite 
    os.makedirs(UPLOAD_FOLDER) #create the new folder with that name

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # This makes the path accessible from anywhere within the Flask application using app.config['UPLOAD_FOLDER'].


#404 page help notice page are broken 
@app.route('/error')
def waiting_web_page():
    image_url = url_for('static', filename='/picture/background/download.jpg')
    return render_template('404index.html')

#function delete row 
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

# replace variable 
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

#function text to num 
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
  
@app.route('/output/<filename>')#download file must be in output folder and specific file name 
def download_file(filename):
    return send_from_directory('output', filename, as_attachment=True)

# main part 
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

@app.route('/account')
def account():
    image_url = url_for('static', filename='/background/bigdatebackground.jpg')
    return render_template('login.html',image_url = image_url)

@app.route('/login')
def login():
    return render_template("login.html")



# đăng ký 
@app.route('/')
def signup():
    return render_template("signup.html")

#giải quyết vấn đề data base
@app.route('/', methods=['POST'])
def signup_process():
    # Lấy dữ liệu từ form
    user = request.form.get('username')
    pw = request.form.get('password')
    email = request.form.get('gmail')

    # Hash mật khẩu (Best practice cho dân Cybersecurity như ông)
    hashed_pw = generate_password_hash(pw, method='pbkdf2:sha256')

    # Lưu vào databa
    new_user = User(username=user, password=hashed_pw, email=email)
    try:
        print("[*] THÔNG TIN ĐANG ĐƯỢC GHI... ")
        db.session.add(new_user)
        db.session.commit()
        print(" Thông tin đã được ghi thành công. ")
        return 
    
    except Exception as e:
        db.session.rollback()
        print(f'[!] dataabase tu choi luu{e}')
        return f"Lỗi rồi! Có thể username hoặc email đã tồn tại as {e}." 
    
mode = "dev" #dev or prod

if __name__ == "__main__":
    if mode == "dev":
        app.run(debug=True, host='0.0.0.0', port=8080)
    elif mode == "prod" :
        print("login to the webpage as http://localhost:8080")
        serve(app, host='0.0.0.0', port=8080, threads=2)
    else :
        print("Unknow command")
        exit
