import sys

sys.path.append("zklib")
from zklib import zklib
import psycopg2
import datetime, time

# Connect to database
currentDB = None
cur = None
try:
    connectDB = psycopg2.connect(database="postgres", user="postgres", password="123", host="127.0.0.1", port="5432")
    print ("Connected database successfully")
    cur = connectDB.cursor()
except:
    print ("Unable to connect to the database")

# Connect to device X628
zk = zklib.ZKLib("192.168.1.201", 4370)
statusConnect = zk.connect()
if statusConnect:
    print ("Connected to device")
else:
    print ("No connected to devive")

# Pulling data
while True:
    if statusConnect:
        attendance = zk.getAttendance()
        # cur.execute("DELETE FROM datatable")
        users = zk.getUser()
        tempDate = zk.getTime().date()
        # Pull data swipe
        for attData in attendance:
            for uid in users:  # Get name user
                if users[uid][0] == attData[0]:
                    nameUser = users[uid][1]
            dataTime = ({"iduser": format(attData[0]), "name": nameUser, "date": format(attData[2].date()),
                         "time": format(attData[2].time()), "method_swipe": format(attData[1])})
            cur.execute(
                "INSERT INTO datatable (iduser,name,date,time,method_swipe) VALUES (%(iduser)s, %(name)s, %(date)s, %(time)s, %(method_swipe)s)",
                dataTime)
        # connectDB.commit()

        # Calculate time
        maxTime = None
        minTime = None
        dateNow = datetime.date.today()

        timeTempIn = datetime.time(9, 0, 0)  # Time in
        timeTempOut = datetime.time(18, 0, 0)  # Time out
        timeTempLate = datetime.time()
        timeTempEarly = datetime.time()
        dataTempDate = None
        for uid in users:
            cur.execute(
                "SELECT iduser FROM timetable WHERE date = '" + str(dateNow) + "' AND iduser = " + str(users[uid][0]) + "")
            dataTempDate = cur.fetchall()
        tempCheck = False
        if dataTempDate == None:
            tempCheck = True
        else:
            tempCheck = False
        if tempCheck:
            for uid in users:
                idUser = users[uid][0]
                maxTime = datetime.time()
                minTime = datetime.time()
                dateNow = datetime.date.today()
                cur.execute(
                    "SELECT time FROM datatable WHERE date = '" + str(dateNow) + "' AND iduser = " + str(idUser) + "")
                dataQuery = cur.fetchall()
                # Sort data after query
                sorted(dataQuery)
                if len(dataQuery) > 0:
                    for i in dataQuery[0]:
                        minTime = i
                    for j in dataQuery[len(dataQuery) - 1]:
                        maxTime = j
                    if minTime <= timeTempIn:
                        timeTempEarly = datetime.time(timeTempIn.hour - minTime.hour, timeTempIn.minute - minTime.minute,
                                                      timeTempIn.second - minTime.second)
                    elif maxTime >= timeTempIn:
                        timeTempLate = datetime.time(maxTime.hour - timeTempIn.hour, maxTime.minute - timeTempIn.minute,
                                                     maxTime.second - timeTempIn.second)
                    dataInsert = ({"iduser": format(idUser), "name": format(users[uid][1]), "timein": format(minTime),
                                   "date": format(dateNow), "timeout": format(maxTime), "timeearly": format(timeTempEarly),
                                   "timelate": format(timeTempLate)})
                    cur.execute(
                        "INSERT INTO timetable (iduser,name,date,timein,timeout,timelate,timeearly) VALUES (%(iduser)s, %(name)s, %(date)s, %(timein)s, %(timeout)s, %(timelate)s,%(timeearly)s)",
                        dataInsert)
                    connectDB.commit()
            print("Pulling data is done")
    else:
        print("Can not pulling data")
        print("Can not connect to device")
    time.sleep(300)
