from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
config = {
  "apiKey": "AIzaSyBAiR8BB_pNp_zhOHfD_prQ9viaR90pc-0",
  "authDomain": "adi-signup.firebaseapp.com",
  "projectId": "adi-signup",
  "storageBucket": "adi-signup.appspot.com",
  "messagingSenderId": "289458113899",
  "appId": "1:289458113899:web:0b89b30d21666e18e4502e",
  "databaseURL":"https://adi-signup-default-rtdb.europe-west1.firebasedatabase.app/" }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
             error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {
            "full_name": request.form['full_name'], "email": request.form['email'],
            "username": request.form['username'],"bio": request.form['bio']
            }
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
             error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        Title = request.form['title']
        text = request.form['text']
        try:
            tweet = {"title": request.form['title'], "text": request.form['text']}
            db.child("tweets").child(UID).set(tweet)
            return redirect(url_for('/all_tweets'))
        except:
             error = "tweet failed"
    return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    tweets = db.child("tweet").get().val()
    return render_template("all_tweets.html", tweets=tweets)
if __name__ == '__main__':
    app.run(debug=True)