import sys
import json
sys.path.append("zklib")
from zklib import zklib
from time import sleep
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from datetime import datetime, date, time
import psycopg2

app = Flask("__name__")

# Connect database
connectDB = None
cur = None
try:
    connectDB = psycopg2.connect(database="postgres", user="postgres", password="123", host="127.0.0.1", port="5432")
    print ("Connected database successfully")
    cur = connectDB.cursor()
except:
    print ("Unable to connect to the database")


# Show data update
@app.route("/")
def showData():
    arrayData = []
    cur.execute("SELECT * FROM timetable")
    data = cur.fetchall()
    for i in data:
        arrayData.insert(0, (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
    return render_template('showData.html', showdata=arrayData)


# hien thi thong ke #######################################################################
@app.route("/report", methods=['GET', 'POST'])
def report():
    k = []
    # if request.method == 'POST':
    #     name = request.form['name']
    #     id = request.form['id']
    #     date = request.form['date']
    #     date1 = request.form['date1']
    #     cur.execute("SELECT * FROM usertable")
    #     usertable = cur.fetchall()
    #     if str(date) != "" and str(date1) != "":
    #         flash(str(date) + " - " + str(date1))
    #         cur.execute("SELECT id, name, SUM(point), SUM(timelate) AS point FROM datatable WHERE date >= '" + str(
    #             date) + "' AND date <= '" + str(date1) + "' GROUP BY id, name ")
    #         dataselect = cur.fetchall()
    #         d1 = datetime.strptime(date1, "%m/%d/%Y")
    #         d = datetime.strptime(date, "%m/%d/%Y")
    #         numberDay = 0

    return render_template('report.html', statistic=k)




############### tao user #########################################
@app.route("/create", methods=['GET', 'POST'])
def forms():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        form = ReusableForm(request.form)
        print form.errors
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            id = request.form['id']
            uid = request.form['uid']
            if statusConnect == False:
                flash('Please connect to fingerprint scanner first !')
            else:
                if id != "" and name != "" and uid != "":
                    temp = 0
                    cur.execute("SELECT * FROM usertable ")
                    usertable = cur.fetchall()
                    for user in usertable:
                        if int(user[1]) == int(id) or int(user[0]) == int(uid):
                            temp = 1
                    if temp == 0:
                        zkteco.set_user(uid=int(uid), name=str(name), privilege=const.USER_DEFAULT,
                                        password=str(password), group_id='', user_id=str(id))
                        flash(' Welcome!  Name: ' + name + " ID:" + id)
                    elif temp == 1:
                        flash('UID or ID already exist')
                else:
                    flash('Error:Please type UID, ID, Name ')
        return render_template('create.html', form=form)


# Delete user
@app.route("/delete", methods=['GET', 'POST'])
def delete():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # else:
    #     form = ReusableForm(request.form)
    #     print form.errors
    #     cur.execute("SELECT * FROM usertable")
    #     usertable = cur.fetchall()
    #     if request.method == 'POST':
    #         name = request.form['name']
    #         id = request.form['id']
    #         uid = request.form['uid']
    #         tempdelete = 0
    #         if statusConnect == False:
    #             flash('Please connect to fingerprint scanner first !')
    #         else:
    #             if id != "" and uid != "" and name != "":
    #                 for user in usertable:
    #                     if int(user[0]) == int(uid):
    #                         tempdelete = 1
    #                     else:
    #                         tempdelete = 2
    #             elif id == "" or uid == "" or name == "":
    #                 flash(' Type ID and UID and name!')
    #         if tempdelete == 2:
    #             flash(' ID and UID does not exist')
    #         elif tempdelete == 1:
    #             zkteco.delete_user(uid=int(uid))
    #             flash('UID:' + str(user[0]) + '. ID: ' + str(user[1]) + '. Name: ' + str(user[2]))
    #             flash(' Deleted!')

    return render_template('delete.html')




# Show report
# @app.route("/report", methods=['GET', 'POST'])
# def get():
#     form = ReusableForm(request.form)
#     print form.errors
#     return render_template('report.html', form=form)

# List user
@app.route('/user')
def user():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        y = []
        cur.execute("SELECT * FROM usertable")
        rows3 = cur.fetchall()
        for data in rows3:
            y.insert(0, (data[0], data[1], data[2], data[3]))
        return render_template('user.html', user=y)


# List student
# @app.route('/useronline/')
# def userOnline():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         y = []
#         y1 = []
#         currentTime = datetime.datetime.now().strftime("%Y-%m-%d")
#         onedayagoTime = date.today() - timedelta(1)
#         twodayagoTime = date.today() - timedelta(2)
#         threedayagoTime = date.today() - timedelta(3)
#         cur.execute("SELECT * FROM usertable")
#         usertable = cur.fetchall()
#         cur.execute("SELECT * FROM datatable")
#         datatable = cur.fetchall()
#         cur.execute("SELECT * FROM datatable WHERE date = " + `str(currentTime)`)
#         datatemp = cur.fetchall()
# 
#         for data in datatemp:
#             if 1000 > data[4] >= 1:
#                 data = list(data)
#                 data[4] = 'co mat'
#                 data = tuple(data)
#             elif 1000000 > data[4] >= 1000:
#                 data = list(data)
#                 data[4] = 'nua ngay'
#                 data = tuple(data)
#             elif data[4] >= 1000000:
#                 data = list(data)
#                 data[4] = 'ca ngay'
#                 data = tuple(data)
#             y.insert(0, (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
#         #### thong ke 3 ngay gan day #######################################
#         for user in usertable:
#             threedayago = cur.execute(
#                 "SELECT point FROM datatable WHERE (date,id)  = " + " ( " + `str(threedayagoTime)` + "," + str(
#                     user[1]) + ")")
#             threedayago = cur.fetchall()
#             twodayago = cur.execute(
#                 "SELECT point FROM datatable WHERE (date,id)  = " + " ( " + `str(twodayagoTime)` + "," + str(
#                     user[1]) + ")")
#             twodayago = cur.fetchall()
#             onedayago = cur.execute(
#                 "SELECT point FROM datatable WHERE (date,id)  = " + " ( " + `str(onedayagoTime)` + "," + str(
#                     user[1]) + ")")
#             onedayago = cur.fetchall()
#             today = cur.execute(
#                 "SELECT point FROM datatable WHERE (date,id)  = " + " ( " + `str(currentTime)` + "," + str(
#                     user[1]) + ")")
#             today = cur.fetchall()
#             for data in twodayago:
#                 twodayago = data[0]
#             for data in onedayago:
#                 onedayago = data[0]
#             for data in threedayago:
#                 threedayago = data[0]
#             for data in today:
#                 today = data[0]
#             #
#             if threedayago == 1000000:
#                 threedayago = "ca ngay"
#             elif threedayago == 1000:
#                 threedayago = "nua ngay"
#             elif not threedayago:
#                 threedayago = "nghi"
#             #
#             if twodayago == 1000000:
#                 twodayago = "ca ngay"
#             elif twodayago == 1000:
#                 twodayago = "nua ngay"
#             elif not twodayago:
#                 twodayago = "nghi"
#             #
#             if onedayago == 1000000:
#                 onedayago = "ca ngay"
#             elif onedayago == 1000:
#                 onedayago = "nua ngay"
#             elif not onedayago:
#                 onedayago = "nghi"
#                 #
#             if not today:
#                 today = "nghi"
#             y1.insert(0, (user[1], user[2], threedayago, twodayago, onedayago, today))
# 
#             for data in datatemp:
#                 if data[1] == user[1]:
#                     y1.remove((user[1], user[2], threedayago, twodayago, onedayago, today))
#         return render_template('userOnline.html', userOnline=y, userOffnline=y1)

# Login
@app.route('/login')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('showData.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if  request.form['username'] == 'admin' and request.form['password'] == '1' :
        session['logged_in'] = True
    return home()
# 
# 
# @app.route("/logout")
# def logout():
#     session['logged_in'] = False
#     return showData()
# 
# 
# @app.route("/")
# def none():
#     session['logged_in'] = False
#     return showData()

if __name__ == "__main__":
    app.run(port=8080)