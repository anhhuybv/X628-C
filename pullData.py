import sys

sys.path.append("zklib")
from zklib import zklib
import psycopg2
import datetime, time
from zk import ZK

# Connect to database
currentDB = None
cur = None
try:
    connectDB = psycopg2.connect(database="postgres", user="postgres", password="123", host="127.0.0.1", port="5432")
    print ("Connected database successfully")
    cur = connectDB.cursor()
except:
    print ("Unable to connect to the database")

# device X628
zk = zklib.ZKLib("192.168.1.201", 4370)
zkt = ZK('192.168.1.201', port=4370, timeout=5)
conZkt = zkt.connect().is_connect

# Pulling data
while True:
    statusConnect = zk.connect()
    if statusConnect:
        print ("Connected to device")
    else:
        print ("No connected to devive")
        print("Pulling")
    if statusConnect:
        users = zkt.get_users()
        attendances = zkt.get_attendance()
        tempDate = zk.getTime().date()
        zkt.get_serialnumber()
        for us in users:
            for att in attendances:
                if us.user_id == att.user_id:
                    dataTime = ({"iduser": format(us.user_id), "name": us.name, "date": format(att.timestamp.date()),
                                 "time": format(att.timestamp.time()), "method_swipe": format(att.status)})
                    cur.execute(
                        "INSERT INTO datatable (iduser,name,date,time,method_swipe) VALUES (%(iduser)s, %(name)s, %(date)s, %(time)s, %(method_swipe)s)",
                        dataTime)
                    connectDB.commit()
        # zkt.clear_attendance()
        # Calculate time
        maxTime = None
        minTime = None
        dateNow = datetime.date.today()

        timeTempIn = datetime.time(9, 0, 0)  # Time in
        timeTempOut = datetime.time(18, 0, 0)  # Time out
        timeTempLate = datetime.time()
        timeTempEarly = datetime.time()
        dataTempDate = [None]
        # Check user
        for us in users:
            cur.execute("SELECT iduser FROM timetable WHERE date = '" + str(dateNow) + "' AND iduser = '" + str(us.user_id) + "'")
            dataTempDate = cur.fetchall()
            if dataTempDate.__len__() == 0:
                uid = us.uid
                idUser = us.user_id
                nameUser = us.name
                maxTime = datetime.time()
                minTime = datetime.time()
                dateNow = datetime.date.today()
                cur.execute("SELECT time FROM datatable WHERE date = '" + str(dateNow) + "' AND iduser = '" + str(
                    idUser) + "'")
                dataQuery = cur.fetchall()
                # Sort data after query
                sorted(dataQuery)
                if len(dataQuery) > 0:
                    for i in dataQuery[0]:
                        minTime = i
                    for j in dataQuery[len(dataQuery) - 1]:
                        maxTime = j
                    if minTime <= timeTempIn:
                        timeTempEarly = datetime.time(timeTempIn.hour - minTime.hour,
                                                      timeTempIn.minute - minTime.minute,
                                                      timeTempIn.second - minTime.second)
                    elif maxTime >= timeTempIn:
                        timeTempLate = datetime.time(maxTime.hour - timeTempIn.hour,
                                                     maxTime.minute - timeTempIn.minute,
                                                     maxTime.second - timeTempIn.second)
                    dataInsert = ({"iduser": format(uid), "name": format(nameUser), "timein": format(minTime),
                                   "date": format(dateNow), "timeout": format(maxTime),
                                   "timeearly": format(timeTempEarly),
                                   "timelate": format(timeTempLate)})
                    cur.execute(
                        "INSERT INTO timetable (iduser,name,date,timein,timeout,timelate,timeearly) VALUES (%(iduser)s, %(name)s, %(date)s, %(timein)s, %(timeout)s, %(timelate)s,%(timeearly)s)",
                        dataInsert)
                    connectDB.commit()
        print("Pulling data is done")
    else:
        print("Can not pulling data")
        print("Can not connect to device")
    time.sleep(60)
