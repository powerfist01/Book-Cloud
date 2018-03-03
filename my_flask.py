from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
conn=sqlite3.connect("book.db")
from os import walk, path

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#from werkzeug.utils import secure_filname
app = Flask(__name__,static_url_path='/static')
app.secret_key = 'some_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_all_filenames():
    fileswalk = walk(app.config['UPLOAD_FOLDER']).__next__()
    foldername = fileswalk[0]
    filenames = fileswalk[2]
    return filenames

@app.route('/')
def index():
    cursor=conn.execute("""SELECT NAME, COUNT FROM BOOKS """)
    result = []
    for name,count in cursor:
        result.append((name,count))
    print(result)
    popular=conn.execute("""SELECT NAME, COUNT FROM BOOKS ORDER BY COUNT DESC LIMIT 10""")
    top = []
    for name,count in popular:
        top.append((name,count))
    print(top)
    return render_template('index.html', data=result, data1=top, data2=len(result))
    
    

@app.route('/book/<filename>')
def book(filename):
    print(filename)
    conn.execute("UPDATE BOOKS SET COUNT=COUNT+? WHERE NAME=?",(1,filename,))
    conn.commit()
    print("count increases")
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/search')
def search():
    query = request.args.get("query").lower()
    files = []
    cursor=conn.execute("""SELECT NAME, COUNT FROM BOOKS """)
    result = []
    for name,count in cursor:
        files.append((name,count));
    for filename,count in files:
        if query in filename.lower():
            print('found something')
            result.append((filename,count))
    return render_template('index.html', search_data=result)



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'no file part'
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(path.join(app.config['UPLOAD_FOLDER'],filename))
        conn.execute("INSERT INTO BOOKS VALUES (NULL,?,?)",(filename,0))
        conn.commit()
        flash('file uploaded!')
    return render_template('upload.html')

@app.route('/database')
def db():
    books=conn.execute("SELECT * FROM BOOKS; ")
    for row in books:
        print(row)
    return "Hello"

app.run(port = 8000, host = '0.0.0.0',debug=False)
