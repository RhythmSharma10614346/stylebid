import os
import bcrypt
from flask import Flask, redirect, render_template, session, url_for, request
import mysql.connector
from flask_mail import Message, Mail
from flask_wtf.csrf import CSRFProtect

from datetime import datetime, timezone

app = Flask(__name__ , static_folder:= "/static")
app.secret_key = 'as)kshued*csmookc@sdcjms]'

UPLOAD_FOLDER = os.path.join('static/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#database-connection 
mydb = mysql.connector.connect(
	host="127.0.0.1",
	user="root",
	password="P@ssword",
	database="webstylebid"
)

cursor = mydb.cursor()

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['DEBUG'] = True

app.config['MAX_CONTENT_PATH'] = 16 * 1000 * 1000
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <stylebidrhythm@gmail.com>'


mail = Mail(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/auction')
def auction():
	return render_template("auction.html")

@app.route('/login')
def loginpage():
	return render_template("login.html")

@app.route('/bids', methods=['GET', 'POST'])
def bids():
     return render_template("bids.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@app.route('/place_bid', methods=['POST'])
def place_bid():
    bid_amount = request.form.get('bid_amount')
    bid_time = datetime.now(timezone.utc)
    
    query = "INSERT INTO bids (bid_amount, bid_time) VALUES (%s, %s)"
    values = (bid_amount, bid_time)
    cursor.execute(query, values)
    mydb.commit()

    return redirect('/bids')

@app.context_processor
def utility_processor():
    def current_time():
        return datetime.utcnow()
    return dict(datetime=datetime, current_time=current_time)
   
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        gender = request.form['gender']
        phone = request.form['phone']

        #converting password to array of bytes

        bytes = password.encode('utf-8')

        salt = bcrypt.gensalt()

        # Hash password with bcrypt
        password = bcrypt.hashpw(bytes, salt)

        print(password)

        # Insert data into DB
        cursor = mydb.cursor()
        sql = "INSERT INTO users (username, email, securepass, address, gender, phone) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (username, email, password, address, gender, phone)
        cursor.execute(sql, values)
        mydb.commit()
        cursor.close()
        
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        users = cursor.fetchone()
        cursor.close()
        

        if users and bcrypt.checkpw(password.encode('utf-8'), users[3].encode('utf-8')):
            session['loggedin'] = True
            session['id'] = users[0]
            session['username'] = users[1]
            msg = 'Logged in successfully !'
            return render_template('auction.html')
        else:
            msg = 'Incorrect email / password !'

    return render_template('success', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)