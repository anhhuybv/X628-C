# coding=<UTF-8>

import sys
sys.path.append("zklib")
from flask import Flask, render_template, request, session, flash
from wtforms import Form, TextField, validators
import os
import psycopg2

DEBUG = True
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


class UserForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])


# Create user
@app.route("/createUser", methods=['GET', 'POST'])
def createUser():
    if session.get('logged_in'):
        userForm = UserForm(request.form)
        print(userForm.errors)
        if request.method == 'POST':
            uid = request.form['uid']
            userid = request.form['userid']
            name = request.form['name']
        if userForm.validate():
            print(userForm.validate())
            flash('Complete append student ' + name)
        return render_template('createUser.html', form=userForm)
    else:
        return render_template('login.html')


# Show data update
@app.route("/")
def showData():
    temp = []
    cur.execute("SELECT * FROM timetable")
    data = cur.fetchall()
    for i in data:
        temp.append(i)
    return render_template('showData.html', showdata=temp)


# Show report
@app.route("/report", methods=['GET', 'POST'])
def report():
    k = []
    return render_template('report.html', statistic=k)


# Delete student
@app.route("/delete", methods=['GET', 'POST'])
def delete():
    return render_template('delete.html')


# List user
@app.route('/user')
def user():
    if session.get('logged_in'):
        user = []
        cur.execute("SELECT * FROM usertable")
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


@app.route("/")
def logout():
    session['logged_in'] = False
    return showData()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(port=8080)
