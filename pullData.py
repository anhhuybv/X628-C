from zklib import zklib
import psycopg2

# Connect to database
currentDB = None
current = None
try:
    connectDB = psycopg2.connect(database="postgres", user = "postgres", password = "123", host = "127.0.0.1", port = "5432")
    print "Connected database successfully"
    current = connectDB.cursor()
except:
    print "Unable to connect to the database"

# Connect to device X628
zk = zklib.ZKLib("192.168.1.200", 4370)
statusConnect = zk.connect()
if statusConnect:
    print "Connected to device"
else:
    print "No connected to devive"

# Pulling data
if statusConnect:
    attendance = zk.getAttendance()
    current.execute("DELETE FROM datatable")

    cout = 0
    dataTemp = attendance[0][0]

    for attData in attendance:
        dataTime = ({"iduser": format(attData[0]), "date": format(attData[2].date()), "time": format(attData[2].time())})
        print "IDUser : %s, Date: %s, Time: %s" % (attData[0],attData[2].date(), attData[2].time())
        current.execute("INSERT INTO datatable (id,date,time) VALUES (%(iduser)s, %(date)s, %(time)s)", dataTime)
        cout += 1
    connectDB.commit()
    connectDB.close()
    current.close()
    print "Done pulling data"
    zk.disconnect()
else:
    print "Can't pulling data"