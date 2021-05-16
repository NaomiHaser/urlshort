#Naomi Haser Cyberark project
##create a url shortener using Python Flask and SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

#Using a daabase to store the long and short url connections- SQLAlchemy (python)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db' ##urls.db is the name of the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #store the object into the database db

@app.before_first_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True) #each will have a unique key
    long = db.Column("long", db.String()) #store the short and long
    short = db.Column("short", db.String(10))

##constructor
    def __init__(self, long, short):
        self.long = long
        self.short = short

def shorten_url():
    allletters = string.ascii_lowercase + string.ascii_uppercase ##52characters
    while True:
        randomletters = random.choices(allletters, k=5)
        randomletters = "".join(randomletters) ##convert list to string
        short_url = Urls.query.filter_by(short=randomletters).first() ##check shorturl does not exist
        if not short_url:
            return randomletters

#decorator function - check the ending of URL to see where to go
#post and get methods to transfer data
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST": ##got a new url to use
        input_url = request.form["name"]
        found_url = Urls.query.filter_by(long=input_url).first()

        if found_url: #if the url is already in database
            return redirect(url_for("show_shorturl", url=found_url.short))
        else: # create short url
            short_url = shorten_url()
            new_url = Urls(input_url, short_url)
            db.session.add(new_url) #add new row to database w new url
            db.session.commit() #changes to db
            return redirect(url_for("show_shorturl", url=short_url))
    else:
        return render_template('url_page.html')

@app.route('/<short_url>') ##redirect to the longer url using the short url
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h2>This short URL does not exist</h2>'

@app.route('/display/<url>')
def show_shorturl(url):
    return render_template('shorturl.html', short_url_display=url)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
