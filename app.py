import os
import bcrypt
from flask import Flask, flash, redirect, jsonify, render_template, session, url_for, request, send_from_directory

import mysql.connector
from flask_mail import Message, Mail
import smtplib
from werkzeug.utils import secure_filename
import re




app = Flask(__name__ , static_folder:= "/static")
app.secret_key = 'as)kshued*csmookc@sdcjms]'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads'
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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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


@app.route('/submit-form', methods=['GET','POST'])
def submit_form():
    # Get the form data
    name = request.form.get('contactname')
    email = request.form.get('contactemail')
    message = request.form.get('query')

    cursor =mydb.cursor()
    cursor.execute('SELECT * FROM webstylebid.message;')
    results = cursor.fetchall()
    cursor.close()

    return render_template('index.html', data=results)

    response = {'Message submitted successfully!'}
    return jsonify(response)


@app.route('/sendemail', methods=['GET', 'POST'])
def send_email(to, subject, template, **kwargs):
    # Get form data
    name = request.form.get['contactname']
    email = request.form.get['conatactemail']
    query = request.form.get['query']

    # Send email
    msg = Message('New query from ' + name, sender=email, recipients=['stylebidrhythm@gmail.com'])
    return 'Mail sent'
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
    return render_template('index.html', data=results)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = contact-form()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Insert data into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        cur.close()

        session['name'] = name
        session['email'] = email
        session['message'] = message

        return redirect(url_for('thank_you'))

    return render_template('contact.html', form=form)

@app.route('/thank-you')
def thank_you():
    name = session.pop('name', None)
    email = session.pop('email', None)
    message = session.pop('message', None)

    return render_template('index.html', name=name, email=email, message=message)
    

#Album form
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        if 'bidder' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/uploaded_file/<path:filename>')
def uploaded_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
        hash = bcrypt.hashpw(bytes, salt)

        print(hash)

        # Insert data into DB
        cursor = mydb.cursor()
        sql = "INSERT INTO users (username, email, securepass, address, gender, phone) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (username, email, password, address, gender, phone)
        cursor.execute(sql, values)
        mydb.commit()
        cursor.close()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM webstylebid.message;')
        users = cursor.fetchall()
        cursor.close()

        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['username'] = users['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'

    return redirect(url_for('success'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/success')
def success():
     flash('Registration completed, Login to Stylebid')
     return render_template('auction.html')
    

if __name__ == '__main__':
    app.run(debug=True)
