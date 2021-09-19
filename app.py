# Importing the required packages/libraries
from flask import Flask,request,render_template,redirect,url_for,session
import  pymysql
from flaskext.mysql import MySQL
import re

app = Flask(__name__)
app.secret_key = "secret key"   # Change this to your secret key (can be anything, it's for extra protection)

mysql = MySQL()

# MySql configuartion
app.config['MYSQL_DATABASE_USER'] = 'root'        # Her provide MySQL database user name
app.config['MYSQL_DATABASE_PASSWORD'] = 'anirudh@1998'   # Here provide your MySQL database password
app.config['MYSQL_DATABASE_DB'] = 'pythongui'     # Here provide the name of your database
app.config['MYSQL_DATABASE_HOST'] = 'localhost'   # Hosting place
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    # create a connection with our MySQL database
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        # Here the 'accoun' is the table that I created in the 'pythongui' database
        cursor.execute('SELECT * FROM accoun WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in 'accoun' table in the database
        if account:
            # Create session data, we can access this data in other routes
            session['username'] = account['username']
            session['email'] = account['email']
            print(session['username'])
            return "Logged successfully"   # Here you can provide the welcome page/logged page code file

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    else:
        # If we enter only one field and try to login this message will show
        msg = "Fill both user name & password column ;"

    return render_template('index.html', msg=msg)



@app.route('/register', methods=['GET', 'POST'])
def register():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)


    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        # 'fullname' is the name that I given for the input tag in html code for 'Your Name' option, similarly following are corresponding input tag names.
        username = request.form['username']
        password = request.form['password']
        confirmpasswd = request.form['re_pass']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accoun WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'user name already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form completely!'
        elif confirmpasswd != password:
            msg = "Password mismatch, Provide confirm password as same as password;"
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accoun VALUES (%s, %s, %s, %s)', (fullname, username, password, email))
            conn.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)

    msg=''

    if request.method == "POST" and 'username' in request.form and 'email' in request.form:
        uname=request.form['username']
        email=request.form['email']

        cursor.execute('select * from accoun where username=%s and email=%s',(uname,email))
        account=cursor.fetchone()

        if account:
            return redirect(url_for('change'))
        else:
            msg = "User name and email are not match"

    else:
        msg = "Invalid"

    return render_template('forgot.html', msg=msg)


@app.route('/change',methods=['GET', 'POST'])
def change():
    conn = mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)

    msg=''

    if request.method=='POST' and 'passwd' in request.form and 'confmpasswd' in request.form:
        password=request.form['passwd']
        confirmpasswd=request.form['confmpasswd']


        if password == confirmpasswd:
            cursor.execute("update accoun set password = %s where username = %s",(password,session['username']))
            conn.commit()
            msg = "Password changed successfully"
        else:
            msg = "New password and confirm password are not matched"

    return render_template('change.html',msg=msg)


if __name__ == "__main__":
    app.run(debug=True)

