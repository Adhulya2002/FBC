from flask import Flask, render_template, request, session, redirect, url_for,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import blockChain
import os
import json
import random

app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234' 
app.config['MYSQL_DB'] = 'FRS'

mysql = MySQL(app)
username= ''

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/index.html')
def home():
    return render_template("index.html")


@app.route('/panel.html')
def panel():
    return render_template('panel.html')

def generate_number():
    return random.randint(1000, 9999)

#temp
@app.route('/panelhome.html',methods=['get'])
def panelhome():
    #username = request.form['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from bookdata")
    print("INN")
    data = cursor.fetchall()
    print(data)
    # Redirect to home page
    return render_template('panelhome.html', data=data, username=username)
    


@app.route('/users.html')
def users():
    return render_template('users.html')


@app.route('/users_home.html', methods=["post", "get"])
def users_home():
    return render_template("users_home.html")


@app.route('/addFRS.html')
def addFRS():
    return render_template('addFRS.html')


@app.route('/book.html')
def book():
    return render_template('book.html')


@app.route('/blockchain.html')
def blockchain():
    return render_template('blockchain.html')


@app.route('/panelregister.html')
def panelregiter():
    return render_template("panelregister.html")

@app.route('/message.html')
def successMessage():
    return render_template('message.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/userslogin', methods=["post", "get"])
def userslogin():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM userdata WHERE username = %s AND password = %s', ([username, password]))
        account = cursor.fetchone()
        if account:
            session['logged'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return render_template('users_home.html', username=username)
        else:
            msg = 'Incorrect username/password!'
        return render_template('users.html', msg=msg)


@app.route("/userssregister", methods=["post", "get"])
def usersregister():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone_number']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM userdata WHERE username = %s', ([username],))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            return render_template('users.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('users.html', msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template('users.html', msg=msg)
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
            return render_template('users.html', msg=msg)
        else:

            cursor.execute('INSERT INTO userdata VALUES (NULL, %s, %s, %s, %s)',
                           (username, password, email, phone))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        return redirect(url_for('users_home', msg=msg, username=username))


@app.route('/adddata', methods=['post', 'get'])
def adddata():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        record_id = request.form['rid']
        vcnum = request.form['cnum']
        vname = request.form['name']
        vage = request.form['age']
        vgender = request.form['gender']
        vphy = request.form['phy']
        vuni = request.form['uni']
        vex = request.form['ex']
        vint = request.form['int']
        vdeath = request.form['death']
        vevidence = request.form['evidence']
        vresult = request.form['result']
        text = record_id  + vcnum + vname + vage + vgender + vphy + vuni + vex + vint + vdeath + vevidence + vresult
        print(type(text))
        print(text)
        if len(text) < 1:
            return redirect(url_for('index'))
        try:
            make_proof = request.form['make_proof']
        except Exception:
            make_proof = False
        blockChain.write_block(text, record_id, vcnum, vname, vage, vgender, vphy, vuni, vex, vint, vdeath, vevidence, vresult, make_proof)

        if not record_id  or not vname or not vage or not vgender or not vphy or not vuni or not vex or not vint or not vdeath or not vevidence or not vresult:
            msg = 'Please Fill All the Fields'
            return render_template('addFRS.html', msg=msg)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO record VALUES (NULL, %s, %s, %s, %s ,%s, %s, %s, %s, %s,%s,%s)',
                           (vname, vage, vgender ,vphy, vuni, vex, vint, vdeath, vevidence, vresult, vcnum))
            mysql.connection.commit()
            msg = 'Data Successfully stored into Block chain'
        return render_template('blockchain.html', msg=msg)


@app.route('/check', methods=['POST'])
def integrity():
    results = blockChain.check_blocks_integrity()
    if request.method == 'POST':
        return render_template('blockchain.html', results=results)
    return redirect(url_for('users_home'))


@app.route('/mining', methods=['POST'])
def mining():
    if request.method == 'POST':
        max_index = int(blockChain.get_next_block())

        for i in range(2, max_index):
            blockChain.get_POW(i)
        return render_template('blockchain.html', querry=max_index)
    return redirect(url_for('users_home'))


@app.route('/bookdata', methods=['post', 'get'])
def book_data():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form['name']
        address = request.form['age']
        forensicdetail = request.form['forensicdetail']
        time = request.form['time']
        patient_id = request.form['patid']
        if not username or not address or not forensicdetail or not time or not patient_id:
            msg = 'Please Fill All the Fields'
            return render_template('book.html', msg=msg)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO bookdata VALUES (NULL, %s, %s, %s, %s, %s, %s)',
                           (username, address, forensicdetail, time, patient_id))
            mysql.connection.commit()
            msg = 'Data Successfully stored into Block chain'
        return render_template('users_home.html', msg=msg)


@app.route('/panellogin', methods=['post', 'get'])
def panellogin():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM panel WHERE username = %s AND password = %s', ([username, password]))
        account = cursor.fetchone()
        if account:
            session['logged'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('book.html')

        else:
            msg = 'Incorrect username/password!'
        return render_template('panel.html', msg=msg)

@app.route('/panelbook', methods=['post', 'get'])
def panelbook():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        ref = ''
        username = request.form['name']
        address = request.form['age']
        forensicdetail = request.form['forensicdetail']
        time = request.form['time']
        patient_id = request.form['patid']
        
        # Generate a random number
        referncenum = generate_number()
        print(referncenum)

        if not username or not address or not forensicdetail or not time or not patient_id:
            msg = 'Please Fill All the Fields'
            return render_template('book.html', msg=msg)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO bookdata VALUES (NULL, %s, %s, %s, %s, %s, %s)',
                           (username, address, forensicdetail, time, patient_id, referncenum))
            mysql.connection.commit()
            msg = 'Data Successfully stored into Block chain'
            print(msg)
        return render_template('message.html', msg=msg, ref=referncenum)

@app.route('/search.html', methods=['GET'])
def search_page():
    return render_template('search.html')

@app.route('/panelsearch', methods=['GET','POST'])
def search_report_page():
    # res = ''
    # msg = ''
    # casenum = request.form['caseno']
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM record WHERE casenum = %s', ([casenum],))
    # account = cursor.fetchone()
    # print(account)
    # if account:
    #     # session['id'] = account['id']    
    #     return render_template('details.html', res=account)
    # else:
    #     msg = 'CASE IN PROGRESS'
    #     return render_template('search.html', res= msg)

    res = {}

    if request.method == 'POST':
        casenum = request.form.get('caseno')

        if casenum:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM record WHERE casenum = %s', ([casenum],))
            account = cursor.fetchone()

            if account:
                return render_template('details.html', res=account)
            
            res = 'CASE IN PROGRESS'
    return render_template('search.html', res=res)

@app.route('/pregister', methods=['post', 'get'])
def pregister():
    if request.method == "get":
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    else:
        msg = ''
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM panel WHERE username = %s', ([username],))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            return render_template('panel.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('panel.html', msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template('panel.html', msg=msg)
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
            return render_template('panel.html', msg=msg)
        else:

            cursor.execute('INSERT INTO panel VALUES (NULL, %s, %s, %s, %s)',
                           (username, password, email, phone))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        return render_template('panel.html', msg=msg, username=username)


@app.route('/test', methods=['GET'])
def test():
    return render_template('panel.html')

@app.route('/outputTable', methods=['GET'])
def generate_html_from_json_folder():
    results = blockChain.check_blocks_integrity()
    return render_template('output.html', results=results)

@app.route('/')
def fetch_row():
    # Fetch data from the database and pass it to the template
    data = fetch_data_from_database()
    return render_template('panelhome.html', data=data)

@app.route('/remove_row/<int:row_id>', methods=['POST'])
def remove_row(row_id):
    # Logic to remove the row from the database
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM bookdata WHERE id = %s', (row_id,))
    mysql.connection.commit()
    
    # Dummy response for demonstration
    #return jsonify({'message': f'Row {row_id} removed successfully'})

# @app.route('/', methods=['POST'])
# def handle_post_request():
#     # Handle other POST requests here
#     return jsonify({'message': 'Request handled successfully'})

def fetch_data_from_database():
    # Logic to fetch data from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM bookdata')
    data = cursor.fetchall()
    data = fetch_data_from_database()
    return render_template('panelhome.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)