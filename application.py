import os

from flask import Flask, session, request, render_template, flash, url_for, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests 
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'prettyprinted'


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('signup.html')
    else: 
        userChek = db.execute('SELECT * from registration where username=:username',
            {'username' : request.form.get('username')}).fetchone() 
        emailChek = db.execute('SELECT * from registration where email=:email',
            {'email' : request.form.get('email')}).fetchone()
        if userChek:
            flash('Username already taken, try a different one', 'danger')
            return render_template('signup.html')
        if emailChek:
            flash('Email already taken, try a different one', 'danger')
            return render_template('signup.html')
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
    if password == password2:
        db.execute('INSERT INTO registration (username, email, password, password2) VALUES (:username, :email, :password, :password2)',
        {'username': username, 'email': email, 'password': password, 'password2': password2})
        flash('Account created', 'success')

        db.commit()
        return redirect('/register')
    else:
        flash('Password does not match','danger')
        return render_template('signup.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('user'):
            return render_template('login.html', session=session['user'])
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
    data=db.execute('Select * from registration where email=:email and password=:password',
                        {'email': email, 'password': password}).fetchall()
    if not data:
        flash('Username/Password does not match', 'danger')
        return redirect('/login')
    else:
        print(data)
        session['user']=True
        session['user']=data[0][1]
        return render_template('search.html')


@app.route('/logout')
def logout():
        session.pop('user', None)
        flash('Logged out succesfully','success')
        return render_template('index.html')
    


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        title = request.form['title']
        title = title.title()
        author = request.form['author']
        year = request.form['year']
        isbn = request.form['isbn']
        list = []
        text = None
        baseUrl = request.base_url

        if title:
            result = db.execute(" SELECT * FROM bookse WHERE title LIKE '%"+title+"%' ;").fetchall()
            text = title
        elif author:
            result = db.execute("SELECT * FROM bookse WHERE author iLIKE '%"+author+"%'").fetchall()
            text = author
        elif year:
            result = db.execute("SELECT * FROM bookse WHERE year iLIKE '%"+year+"%'").fetchall()
            text = year
        else:
            result = db.execute(" SELECT * FROM bookse WHERE isbn LIKE '%"+isbn+"%' ;").fetchall()
            text = isbn
        if result: 
            for i in result : 
                list.append(i)
            itemsCount = len(list)
            return render_template('search.html', baseUrl = baseUrl,  items = list, msg = "Search result found", text = text , itemsCount = itemsCount)
        else:
            flash('We could not find any possible matching results, please try again', 'danger')
            return render_template('search.html', msgNo = "Sorry! No books found" , text = text)
    

@app.route("/review/<isbn>", methods=["GET", "POST"])
def review(isbn):
    isbn = isbn
    username = session['user']

    apiCall = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "j48RmSu6UOD6a5ko9dRR3w", "isbns": isbn })
    apidata = apiCall.json()
    dbdata = db.execute(" SELECT * FROM bookse WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    dbreviews = db.execute('SELECT * FROM reviews WHERE isbn = :isbn', {'isbn': isbn}).fetchall()
    revcheck = db.execute('SELECT * FROM public.reviews WHERE isbn = :isbn and username = :username ', {'isbn': isbn, 'username': username}).fetchall()
    list = []

    if request.method == "POST":
        if revcheck: 
            flash('You alreaddy submitted a review on this book', 'danger')
        else:
            uses = session['user']
            rat = request.form['rating']
            rev = request.form['review']
            isbn = isbn
            db.execute("INSERT into reviews (username, rating, review, isbn) Values (:uses, :rating, :review, :isbn)", {'uses': uses, 'rating': rat, 'review': rev, 'isbn':isbn})
            db.commit()
            flash('You have submitted your review succesfully', 'success')
            return render_template('search.html')           
    if apiCall:
        if dbreviews:            
            for i in dbreviews: 
                list.append(i)
        return render_template('review.html', items = list, apidata = apidata, dbdata = dbdata, dbreviews = dbreviews, isbn = isbn)
    else:
        return render_template('review.html')
    



        
@app.route("/api/<isbn>", methods=['GET'])
def api(isbn):     
    data=db.execute("SELECT * FROM bookse WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    if data==None:
        return render_template('error.html')

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "j48RmSu6UOD6a5ko9dRR3w", "isbns": isbn})
    average_rating=res.json()['books'][0]['average_rating']
    work_ratings_count=res.json()['books'][0]['work_ratings_count']

    x = {
    "title": data.title,
    "author": data.author,
    "year": data.year,
    "isbn": isbn,
    "review_count": work_ratings_count,
    "average_rating": average_rating
    }

    return  jsonify(x)

if __name__ == '__main__':
    app.run(debug =True)