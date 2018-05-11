import sys

sys.path.append("zklib")
from flask import Flask, render_template, request, session
from wtforms import Form, TextField, validators
import os, datetime, psycopg2
from zk import ZK

app = Flask("__name__")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# Connect database
connectDB = None
cur = None
try:
    connectDB = psycopg2.connect(database="postgres", user="postgres", password="123", host="127.0.0.1", port="5432")
    print ("Connected database successfully")
    cur = connectDB.cursor()
except:
    print ("Unable to connect to the database")

zkt = ZK('192.168.1.201', port=4370, timeout=5)
zkt.connect()
conZkt = zkt.is_connect


class UserForm(Form):
    uid = TextField('uid:', validators=[validators.required(), validators.Length(min=1, max=35)])
    id = TextField('iduser:', validators=[validators.required(), validators.Length(min=1, max=35)])
    name = TextField('name:', validators=[validators.required(), validators.Length(min=1, max=35)])


# Create user
@app.route("/createUser", methods=['GET', 'POST'])
def createUser():
    if session.get('logged_in'):
        userForm = UserForm(request.form)
        if request.method == 'POST':
            uid = request.form['uid']
            iduser = request.form['iduser']
            name = request.form['name']
            phoneNumber = request.form['phonenumber']
            email = request.form['email']
            print(phoneNumber)
            print(email)
            cur.execute("SELECT uid FROM usertable WHERE uid = '" + str(uid) + "' and iduser = '" + str(iduser) + "'")
            data = cur.fetchall()
            if data.__len__() == 0:
                user = ({"uid": format(uid), "iduser": format(iduser), "name": format(name), "phonenumber":format(phoneNumber),"email":format(email)})
                cur.execute("INSERT INTO usertable (uid,iduser,name,phonenumber,email) VALUES (%(uid)s, %(iduser)s, %(name)s, %(phonenumber)s, %(email)s)", user)
                connectDB.commit()
        return render_template('createUser.html', form=userForm)
    else:
        return render_template('login.html')


# Delete user
@app.route("/deleteUser", methods=['GET', 'POST'])
def delete():
    if session.get('logged_in'):
        deleteUser = UserForm(request.form)
        if request.method == 'POST':
            iduser = request.form['iduser']
            print(iduser)
            user = ({"iduser": format(iduser)})
            cur.execute("DELETE FROM usertable WHERE iduser = '" + str(iduser) + "'", user)
            if conZkt:
                connectDB.commit()
                users = zkt.get_users()
                for user in users:
                    if user.uid == iduser:
                        zkt.delete_user(uid=int(iduser))
        return render_template('deleteUser.html', form=deleteUser)
    else:
        return render_template('login.html')


# Show data update
@app.route("/")
def showData():
    arrayData = []
    cur.execute("SELECT * FROM timetable")
    data = cur.fetchall()
    for i in data:
        arrayData.append(i)
    return render_template('showData.html', showdata=arrayData)


# Show report day
@app.route("/reportDay", methods=['GET', 'POST'])
def reportDay():
    arrayData = []
    dateNow = datetime.datetime.now().date()
    cur.execute("SELECT * FROM timetable WHERE date = '" + str(dateNow) + "'")
    data = cur.fetchall()
    for i in data:
        arrayData.append(i)
    return render_template('reportDay.html', statistic=arrayData)


# Show report week
@app.route("/reportWeek", methods=['GET', 'POST'])
def reportWeek():
    arrayData = []
    dateNow = datetime.datetime.now().date()
    cur.execute("SELECT * FROM timetable WHERE (date >= date '" + str(dateNow) + "' - integer '7') AND date <= '" + str(
        dateNow) + "'")
    data = cur.fetchall()
    for i in data:
        arrayData.append(i)
    return render_template('reportWeek.html', statistic=arrayData)


# Show report month
@app.route("/reportMonth", methods=['GET', 'POST'])
def reportMonth():
    arrayData = []
    dateNow = datetime.datetime.now().date()
    tempDate = datetime.datetime.now().day
    tempDate -= 1
    cur.execute("SELECT * FROM timetable WHERE (date >= date '" + str(dateNow) + "' - integer '" + str(
        tempDate) + "') AND date <= '" + str(dateNow) + "'")
    data = cur.fetchall()
    for i in data:
        arrayData.append(i)
    return render_template('reportMonth.html', statistic=arrayData)


# List user
@app.route('/user')
def user():
    if session.get('logged_in'):
        user = []
        cur.execute("SELECT iduser,name,phonenumber,email FROM usertable")
        data = cur.fetchall()
        for i in data:
            user.append(i)
        return render_template('user.html', users=user)
    else:
        return render_template('login.html')


# Login
@app.route('/login')
def admin():
    if session.get('logged_in'):
        return render_template('admin.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == '1':
        session['logged_in'] = True
    else:
        session['logged_in'] = False
    return admin()


@app.route("/login")
def logout():
    session['logged_in'] = False
    print(session['logged_in'])
    return showData()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=1010, debug=False)
