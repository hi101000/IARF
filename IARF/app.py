from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from datetime import date
from werkzeug.utils import secure_filename
import os


app=Flask(__name__)
UPLOAD_FOLDER = 'static/submissions'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav', 'mkv', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(12).hex()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

print("listening at: http://127.0.0.1:8080")

@app.route("/")
def index():
    with open("visits.txt", "r") as f:
        visits = int(f.read())
        visits += 1
    with open("visits.txt", "w") as f:
        f.write(str(visits))
    return render_template("index.html", vis = visits)

@app.route('/articles')
def articles():
    con = sqlite3.connect("articles.db")
    cur = con.cursor()
    arts = {}
    res = cur.execute("SELECT title, path FROM Articles")
    for article in res.fetchall():
        arts[article[0]] = article[1]
    con.commit()
    con.close()
    return render_template("Articles.html", articles = arts)

@app.route("/articles/<folder>/<art>")
def article(folder, art):
    return render_template("article.html", fname = art, folder = folder)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/submission")
def submission():
    return render_template("submition.html")

@app.route("/submit", methods = ['GET','POST'])
def submit():
    day = str(date.today()).split('-')
    if request.method == 'POST':
        file = request.files['content']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.system(f"touch {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            split_tup = os.path.splitext(filename)
            ext = split_tup[1]
            os.system(f"mv {os.path.join(app.config['UPLOAD_FOLDER'], filename)} {os.path.join(app.config['UPLOAD_FOLDER'], (request.form['title']+ext))}")
        con = sqlite3.connect("articles.db")
        cur = con.cursor()
        cur.execute(f"""
                    INSERT INTO Submissions 
                    (Date, Month, Year, Title, Submitter, Description) 
                    VALUES 
                    ({int(day[2])}, {int(day[1])}, {int(day[0])}, '{request.form['title']}', '{request.form['name']}', '{request.form['description']}')
                    """)
        con.commit()
        con.close()
        return render_template("redirect_to.html", page="index")
    
@app.route("/to_Selim")
def to_selim():
    return render_template("Selim.html")

@app.route('/ASBOT')
def ASBOT():
    return render_template("ASBOT.html")